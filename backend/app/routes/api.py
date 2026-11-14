"""Everlasting Bloom Studio — REST API blueprint.

Endpoints:
  /api/health                      -> backend health
  /api/hermes/*                    -> Hermes Agent integration (real CLI)
  /api/universe/*                  -> Everlasting Bloom fan content
  /api/studio/*                    -> Everbloom Studio projects
  /api/uploads/*                   -> gallery asset uploads
  /api/auth/*                      -> session-based login (studio admin)

All mutating endpoints require an authenticated admin session except where
noted. No Hermes secrets or credentials are ever returned.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from typing import Optional

from flask import Blueprint, jsonify, request, current_app, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from ..config import DATA_DIR, UPLOADS_DIR
from ..models import (
    db, User, Character, TimelineEntry, Memory, GalleryAsset,
    StudioProject, HermesIntegrationStatus, ContentType, ProjectType,
)

api_bp = Blueprint("api", __name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _require_admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        return jsonify({"error": "forbidden", "message": "admin required"}), 403
    return None


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_content_type(value, default=ContentType.CANON):
    if value and hasattr(ContentType, value.upper()):
        return ContentType[value.upper()]
    return default


def _parse_project_type(value, default=ProjectType.DOCUMENT):
    if value and hasattr(ProjectType, value.upper()):
        return ProjectType[value.upper()]
    return default


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "png", "jpg", "jpeg", "gif", "webp", "svg"
    }


# ---------------------------------------------------------------------------
# Hermes Agent integration (real CLI — never simulated)
# ---------------------------------------------------------------------------

def _run_hermes(args: list[str], timeout: int = 30):
    """Run a `hermes` CLI subcommand safely. Returns (returncode, stdout, stderr).

    Only subcommands in current_app.config["HERMES_ALLOWED_COMMANDS"] are
    permitted. No arbitrary shell execution.
    """
    allowed = current_app.config.get("HERMES_ALLOWED_COMMANDS", [])
    if not args or args[0] not in allowed:
        return 1, "", f"command not allowed: {args[0] if args else '(empty)'}"

    cli = current_app.config.get("HERMES_CLI", "hermes")
    home = current_app.config.get("HERMES_HOME")
    env = None
    if home:
        env = dict(os.environ)
        env["HERMES_HOME"] = home

    profile = current_app.config.get("HERMES_PROFILE")
    cmd = [cli]
    if profile:
        cmd += ["--profile", profile]
    cmd += args

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, env=env
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return 127, "", "hermes CLI not found on PATH"
    except subprocess.TimeoutExpired:
        return 124, "", f"hermes command timed out after {timeout}s"
    except Exception as exc:  # pragma: no cover - defensive
        return 1, "", f"hermes invocation error: {exc}"


@api_bp.get("/hermes/status")
def hermes_status():
    rc, out, err = _run_hermes(["status"])
    row = HermesIntegrationStatus.query.first()
    if not row:
        row = HermesIntegrationStatus()
        db.session.add(row)
    row.hermes_cli_available = (rc == 0)
    row.last_check_at = datetime.now(timezone.utc)
    if rc != 0:
        row.last_error = err.strip() or out.strip()
    else:
        row.last_error = None
        row.hermes_version = _parse_version(out)
    row.profile = current_app.config.get("HERMES_PROFILE")
    db.session.commit()

    return jsonify({
        "available": rc == 0,
        "stdout": out,
        "stderr": err,
        "returncode": rc,
        "profile": row.profile,
    }), 200


def _parse_version(stdout: str) -> Optional[str]:
    for line in stdout.splitlines():
        if "version" in line.lower():
            parts = line.split()
            for p in parts:
                if p.startswith("v") or (p[0].isdigit() if p else False):
                    return p.strip()
    return None


@api_bp.get("/hermes/doctor")
def hermes_doctor():
    rc, out, err = _run_hermes(["doctor"])
    return jsonify({"returncode": rc, "stdout": out, "stderr": err}), 200


@api_bp.get("/hermes/skills")
def hermes_skills():
    rc, out, err = _run_hermes(["skills"])
    return jsonify({"returncode": rc, "stdout": out, "stderr": err}), 200


@api_bp.get("/hermes/memory")
def hermes_memory():
    rc, out, err = _run_hermes(["memory"])
    return jsonify({"returncode": rc, "stdout": out, "stderr": err}), 200


@api_bp.get("/hermes/sessions")
def hermes_sessions():
    rc, out, err = _run_hermes(["sessions"])
    return jsonify({"returncode": rc, "stdout": out, "stderr": err}), 200


@api_bp.get("/hermes/logs")
def hermes_logs():
    rc, out, err = _run_hermes(["logs"])
    return jsonify({"returncode": rc, "stdout": out, "stderr": err}), 200


@api_bp.get("/hermes/config")
def hermes_config():
    """Return sanitized config keys — secrets are masked by the CLI itself."""
    rc, out, err = _run_hermes(["config", "view"])
    return jsonify({"returncode": rc, "stdout": out, "stderr": err}), 200


@api_bp.get("/hermes/profile")
def hermes_profile():
    rc, out, err = _run_hermes(["profile", "list"])
    return jsonify({"returncode": rc, "stdout": out, "stderr": err}), 200


@api_bp.get("/hermes/security")
def hermes_security():
    rc, out, err = _run_hermes(["security"])
    return jsonify({"returncode": rc, "stdout": out, "stderr": err}), 200


# ---------------------------------------------------------------------------
# Auth (studio admin only)
# ---------------------------------------------------------------------------

@api_bp.post("/auth/login")
def auth_login():
    body = request.get_json(silent=True) or {}
    username = body.get("username", "")
    password = body.get("password", "")
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "invalid_credentials"}), 401
    if not user.is_active:
        return jsonify({"error": "account_disabled"}), 403
    login_user(user)
    return jsonify({"user": user.to_dict()}), 200


@api_bp.post("/auth/logout")
@login_required
def auth_logout():
    logout_user()
    return jsonify({"ok": True}), 200


@api_bp.get("/auth/me")
def auth_me():
    if not current_user.is_authenticated:
        return jsonify({"authenticated": False}), 200
    return jsonify({"authenticated": True, "user": current_user.to_dict()}), 200


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@api_bp.get("/health")
def api_health():
    return jsonify({"status": "ok", "service": "everlasting-bloom-studio-backend"}), 200


# ---------------------------------------------------------------------------
# Universe: Characters
# ---------------------------------------------------------------------------

@api_bp.get("/universe/characters")
def universe_list_characters():
    q = Character.query
    search = request.args.get("search")
    content_type = request.args.get("content_type")
    if search:
        like = f"%{search}%"
        q = q.filter(Character.name.ilike(like) | Character.display_name.ilike(like))
    if content_type:
        q = q.filter_by(content_type=_parse_content_type(content_type))
    characters = q.order_by(Character.name.asc()).all()
    return jsonify([c.to_dict() for c in characters]), 200


@api_bp.get("/universe/characters/<int:character_id>")
def universe_get_character(character_id: int):
    c = db.session.get(Character, character_id)
    if not c:
        return jsonify({"error": "not_found"}), 404
    return jsonify(c.to_dict()), 200


@api_bp.post("/universe/characters")
@login_required
def universe_create_character():
    check = _require_admin()
    if check:
        return check
    body = request.get_json(silent=True) or {}
    name = body.get("name", "").strip()
    if not name:
        return jsonify({"error": "name_required"}), 400
    c = Character(
        name=name,
        display_name=body.get("display_name"),
        description=body.get("description"),
        content_type=_parse_content_type(body.get("content_type")),
        image_url=body.get("image_url"),
        is_ancient_hero=bool(body.get("is_ancient_hero", False)),
        is_purelily=bool(body.get("is_purelily", False)),
    )
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201


@api_bp.patch("/universe/characters/<int:character_id>")
@login_required
def universe_update_character(character_id: int):
    check = _require_admin()
    if check:
        return check
    c = db.session.get(Character, character_id)
    if not c:
        return jsonify({"error": "not_found"}), 404
    body = request.get_json(silent=True) or {}
    for field in ("name", "display_name", "description", "image_url"):
        if field in body:
            setattr(c, field, body[field])
    if "content_type" in body:
        c.content_type = _parse_content_type(body["content_type"])
    if "is_ancient_hero" in body:
        c.is_ancient_hero = bool(body["is_ancient_hero"])
    if "is_purelily" in body:
        c.is_purelily = bool(body["is_purelily"])
    db.session.commit()
    return jsonify(c.to_dict()), 200


@api_bp.delete("/universe/characters/<int:character_id>")
@login_required
def universe_delete_character(character_id: int):
    check = _require_admin()
    if check:
        return check
    c = db.session.get(Character, character_id)
    if not c:
        return jsonify({"error": "not_found"}), 404
    db.session.delete(c)
    db.session.commit()
    return jsonify({"ok": True}), 200


# ---------------------------------------------------------------------------
# Universe: Timeline entries
# ---------------------------------------------------------------------------

@api_bp.get("/universe/timeline")
def universe_list_timeline():
    q = TimelineEntry.query
    search = request.args.get("search")
    content_type = request.args.get("content_type")
    character_id = request.args.get("character_id", type=int)
    if search:
        like = f"%{search}%"
        q = q.filter(TimelineEntry.title.ilike(like) | TimelineEntry.description.ilike(like))
    if content_type:
        q = q.filter_by(content_type=_parse_content_type(content_type))
    if character_id:
        q = q.filter_by(character_id=character_id)
    entries = q.order_by(TimelineEntry.event_date.asc().nullslast(), TimelineEntry.created_at.desc()).all()
    return jsonify([e.to_dict() for e in entries]), 200


@api_bp.post("/universe/timeline")
@login_required
def universe_create_timeline():
    check = _require_admin()
    if check:
        return check
    body = request.get_json(silent=True) or {}
    title = body.get("title", "").strip()
    if not title:
        return jsonify({"error": "title_required"}), 400
    e = TimelineEntry(
        title=title,
        event_date=body.get("event_date"),
        description=body.get("description"),
        content_type=_parse_content_type(body.get("content_type")),
        character_id=body.get("character_id"),
        image_url=body.get("image_url"),
    )
    db.session.add(e)
    db.session.commit()
    return jsonify(e.to_dict()), 201


@api_bp.patch("/universe/timeline/<int:entry_id>")
@login_required
def universe_update_timeline(entry_id: int):
    check = _require_admin()
    if check:
        return check
    e = db.session.get(TimelineEntry, entry_id)
    if not e:
        return jsonify({"error": "not_found"}), 404
    body = request.get_json(silent=True) or {}
    for field in ("title", "event_date", "description", "image_url"):
        if field in body:
            setattr(e, field, body[field])
    if "content_type" in body:
        e.content_type = _parse_content_type(body["content_type"])
    if "character_id" in body:
        e.character_id = body["character_id"]
    db.session.commit()
    return jsonify(e.to_dict()), 200


@api_bp.delete("/universe/timeline/<int:entry_id>")
@login_required
def universe_delete_timeline(entry_id: int):
    check = _require_admin()
    if check:
        return check
    e = db.session.get(TimelineEntry, entry_id)
    if not e:
        return jsonify({"error": "not_found"}), 404
    db.session.delete(e)
    db.session.commit()
    return jsonify({"ok": True}), 200


# ---------------------------------------------------------------------------
# Universe: Memories
# ---------------------------------------------------------------------------

@api_bp.get("/universe/memories")
def universe_list_memories():
    q = Memory.query
    search = request.args.get("search")
    content_type = request.args.get("content_type")
    character_id = request.args.get("character_id", type=int)
    is_tribute = request.args.get("is_tribute")
    if search:
        like = f"%{search}%"
        q = q.filter(Memory.title.ilike(like) | Memory.body.ilike(like))
    if content_type:
        q = q.filter_by(content_type=_parse_content_type(content_type))
    if character_id:
        q = q.filter_by(character_id=character_id)
    if is_tribute is not None:
        q = q.filter_by(is_tribute=is_tribute.lower() == "true")
    memories = q.order_by(Memory.created_at.desc()).all()
    return jsonify([m.to_dict() for m in memories]), 200


@api_bp.post("/universe/memories")
@login_required
def universe_create_memory():
    check = _require_admin()
    if check:
        return check
    body = request.get_json(silent=True) or {}
    title = body.get("title", "").strip()
    if not title:
        return jsonify({"error": "title_required"}), 400
    m = Memory(
        title=title,
        body=body.get("body"),
        content_type=_parse_content_type(body.get("content_type"), ContentType.PERSONAL),
        character_id=body.get("character_id"),
        image_url=body.get("image_url"),
        is_tribute=bool(body.get("is_tribute", False)),
    )
    db.session.add(m)
    db.session.commit()
    return jsonify(m.to_dict()), 201


@api_bp.patch("/universe/memories/<int:memory_id>")
@login_required
def universe_update_memory(memory_id: int):
    check = _require_admin()
    if check:
        return check
    m = db.session.get(Memory, memory_id)
    if not m:
        return jsonify({"error": "not_found"}), 404
    body = request.get_json(silent=True) or {}
    for field in ("title", "body", "image_url"):
        if field in body:
            setattr(m, field, body[field])
    if "content_type" in body:
        m.content_type = _parse_content_type(body["content_type"])
    if "character_id" in body:
        m.character_id = body["character_id"]
    if "is_tribute" in body:
        m.is_tribute = bool(body["is_tribute"])
    db.session.commit()
    return jsonify(m.to_dict()), 200


@api_bp.delete("/universe/memories/<int:memory_id>")
@login_required
def universe_delete_memory(memory_id: int):
    check = _require_admin()
    if check:
        return check
    m = db.session.get(Memory, memory_id)
    if not m:
        return jsonify({"error": "not_found"}), 404
    db.session.delete(m)
    db.session.commit()
    return jsonify({"ok": True}), 200


# ---------------------------------------------------------------------------
# Universe: Gallery assets
# ---------------------------------------------------------------------------

@api_bp.get("/universe/gallery")
def universe_list_gallery():
    assets = GalleryAsset.query.order_by(GalleryAsset.created_at.desc()).all()
    return jsonify([a.to_dict() for a in assets]), 200


@api_bp.post("/universe/gallery")
@login_required
def universe_upload_gallery():
    check = _require_admin()
    if check:
        return check
    if "file" not in request.files:
        return jsonify({"error": "file_required"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "filename_required"}), 400
    if not _allowed_file(file.filename):
        return jsonify({"error": "file_type_not_allowed"}), 400
    filename = secure_filename(file.filename)
    save_path = UPLOADS_DIR / filename
    if save_path.exists():
        stem = filename.rsplit(".", 1)[0]
        ext = filename.rsplit(".", 1)[1]
        filename = f"{stem}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.{ext}"
        save_path = UPLOADS_DIR / filename
    file.save(str(save_path))
    asset = GalleryAsset(
        filename=filename,
        original_name=file.filename,
        mime_type=file.mimetype,
        file_path=str(save_path),
        file_size=save_path.stat().st_size,
        alt_text=request.form.get("alt_text"),
        uploaded_by=current_user.username if current_user.is_authenticated else None,
    )
    db.session.add(asset)
    db.session.commit()
    return jsonify(asset.to_dict()), 201


@api_bp.get("/universe/gallery/<int:asset_id>/file")
def universe_get_gallery_file(asset_id: int):
    asset = db.session.get(GalleryAsset, asset_id)
    if not asset:
        return jsonify({"error": "not_found"}), 404
    directory = os.path.dirname(asset.file_path)
    basename = os.path.basename(asset.file_path)
    return send_from_directory(directory, basename, mimetype=asset.mime_type)


@api_bp.delete("/universe/gallery/<int:asset_id>")
@login_required
def universe_delete_gallery(asset_id: int):
    check = _require_admin()
    if check:
        return check
    asset = db.session.get(GalleryAsset, asset_id)
    if not asset:
        return jsonify({"error": "not_found"}), 404
    try:
        if os.path.exists(asset.file_path):
            os.remove(asset.file_path)
    except OSError:
        pass
    db.session.delete(asset)
    db.session.commit()
    return jsonify({"ok": True}), 200


# ---------------------------------------------------------------------------
# Universe: Search (combined)
# ---------------------------------------------------------------------------

@api_bp.get("/universe/search")
def universe_search():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"characters": [], "timeline": [], "memories": []}), 200
    like = f"%{q}%"
    characters = Character.query.filter(
        Character.name.ilike(like) | Character.description.ilike(like)
    ).all()
    timeline = TimelineEntry.query.filter(
        TimelineEntry.title.ilike(like) | TimelineEntry.description.ilike(like)
    ).all()
    memories = Memory.query.filter(
        Memory.title.ilike(like) | Memory.body.ilike(like)
    ).all()
    return jsonify({
        "characters": [c.to_dict() for c in characters],
        "timeline": [e.to_dict() for e in timeline],
        "memories": [m.to_dict() for m in memories],
    }), 200


# ---------------------------------------------------------------------------
# Studio: Projects
# ---------------------------------------------------------------------------

@api_bp.get("/studio/projects")
def studio_list_projects():
    projects = StudioProject.query.order_by(
        StudioProject.last_opened_at.desc().nullslast(),
        StudioProject.updated_at.desc(),
    ).all()
    return jsonify([p.to_dict() for p in projects]), 200


@api_bp.get("/studio/projects/<project_id>")
def studio_get_project(project_id: str):
    p = db.session.get(StudioProject, project_id)
    if not p:
        return jsonify({"error": "not_found"}), 404
    return jsonify(p.to_dict()), 200


@api_bp.post("/studio/projects")
@login_required
def studio_create_project():
    check = _require_admin()
    if check:
        return check
    import uuid
    body = request.get_json(silent=True) or {}
    title = body.get("title", "").strip() or "Untitled Project"
    pid = body.get("id") or str(uuid.uuid4())
    if db.session.get(StudioProject, pid):
        return jsonify({"error": "project_id_exists"}), 409
    p = StudioProject(
        id=pid,
        title=title,
        description=body.get("description"),
        project_type=_parse_project_type(body.get("project_type")),
        state_json=json.dumps(body.get("state")) if body.get("state") is not None else None,
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201


@api_bp.patch("/studio/projects/<project_id>")
@login_required
def studio_update_project(project_id: str):
    check = _require_admin()
    if check:
        return check
    p = db.session.get(StudioProject, project_id)
    if not p:
        return jsonify({"error": "not_found"}), 404
    body = request.get_json(silent=True) or {}
    if "title" in body:
        p.title = body["title"]
    if "description" in body:
        p.description = body["description"]
    if "project_type" in body:
        p.project_type = _parse_project_type(body["project_type"])
    if "state" in body:
        p.state_json = json.dumps(body["state"])
    if body.get("touch_last_opened"):
        p.last_opened_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify(p.to_dict()), 200


@api_bp.delete("/studio/projects/<project_id>")
@login_required
def studio_delete_project(project_id: str):
    check = _require_admin()
    if check:
        return check
    p = db.session.get(StudioProject, project_id)
    if not p:
        return jsonify({"error": "not_found"}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({"ok": True}), 200


# ---------------------------------------------------------------------------
# Seed: create default admin if none exists
# ---------------------------------------------------------------------------

def ensure_default_admin() -> None:
    if not User.query.filter_by(is_admin=True).first():
        u = User(username="admin", is_admin=True, is_active=True)
        u.set_password("admin")
        db.session.add(u)
        db.session.commit()
