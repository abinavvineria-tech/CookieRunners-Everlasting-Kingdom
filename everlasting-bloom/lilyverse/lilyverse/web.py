"""Flask web application for LilyVerse.

Shares the same JSON data store as the CLI. CSRF protection, input validation,
and safe error handling are enabled by default. Debug mode is off unless
LILYVERSE_DEBUG=1.
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from lilyverse.models import ValidationError
from lilyverse.services import LilyVerseService
from lilyverse.storage import StorageError, TimelineStorage


def create_app(storage: TimelineStorage | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.environ.get("LILYVERSE_SECRET_KEY") or os.urandom(24)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    if storage is None:
        storage = TimelineStorage()
    service = LilyVerseService(storage)

    # ------------------------------------------------------------------ #
    # CSRF protection for state-changing requests
    # ------------------------------------------------------------------ #
    @app.before_request
    def _csrf_protect():
        if request.method in ("POST", "PUT", "DELETE", "PATCH"):
            token = request.form.get("csrf_token") or request.headers.get("X-CSRFToken")
            if not token or token != session.get("csrf_token"):
                abort(403)

    @app.context_processor
    def _inject_globals():
        def _csrf_token():
            return session.get("csrf_token") or str(uuid.uuid4())

        return {
            "site_name": "LilyVerse",
            "tagline": "One Lily. Countless Memories. An Eternal Bloom.",
            "csrf_token": _csrf_token,
            "unofficial_label": True,
        }

    @app.before_request
    def _ensure_csrf():
        if "csrf_token" not in session:
            session["csrf_token"] = str(uuid.uuid4())

    # ------------------------------------------------------------------ #
    # Routes
    # ------------------------------------------------------------------ #
    @app.route("/")
    def index():
        milestones = service.list_milestones(sort="newest")[:12]
        stats = service.stats()
        return render_template(
            "index.html",
            events=milestones,
            stats=stats,
        )

    @app.route("/timeline")
    def timeline():
        character = request.args.get("character") or None
        category = request.args.get("category") or None
        sort = request.args.get("sort", "oldest")
        query = request.args.get("q") or None
        milestones = service.list_milestones(
            character=character, category=category, sort=sort, query=query
        )
        characters = service.known_characters()
        categories = sorted({m.category for m in service.storage.list_milestones()})
        return render_template(
            "timeline.html",
            events=milestones,
            characters=characters,
            categories=categories,
            selected_character=character,
            selected_category=category,
            sort=sort,
            query=query or "",
        )

    @app.route("/timeline/<milestone_id>")
    def timeline_detail(milestone_id):
        m = service.get_milestone(milestone_id)
        if m is None:
            abort(404)
        return render_template("timeline_detail.html", m=m)

    @app.route("/timeline/add", methods=["GET", "POST"])
    def timeline_add():
        if request.method == "POST":
            raw = {
                "title": request.form.get("title", "").strip(),
                "date": request.form.get("date", "").strip() or None,
                "character": request.form.get("character", "").strip(),
                "category": request.form.get("category", "").strip(),
                "entry_type": request.form.get("entry_type", "personal memory").strip(),
                "description": request.form.get("description", "").strip(),
                "source": request.form.get("source", "personal").strip(),
            }
            try:
                m = service.add_milestone(raw)
                flash(f"Added milestone {m.id}: {m.title}", "success")
                return redirect(url_for("timeline_detail", milestone_id=m.id))
            except ValidationError as exc:
                flash(str(exc), "error")
            except StorageError as exc:
                flash(str(exc), "error")
        characters = service.known_characters()
        entry_types = list(ENTRY_TYPES_FOR_WEB)
        categories = sorted({m.category for m in service.storage.list_milestones()})
        return render_template(
            "timeline_add.html",
            characters=characters,
            entry_types=entry_types,
            categories=categories,
        )

    @app.route("/timeline/edit/<milestone_id>", methods=["GET", "POST"])
    def timeline_edit(milestone_id):
        m = service.get_milestone(milestone_id)
        if m is None:
            abort(404)
        if request.method == "POST":
            raw = {
                "title": request.form.get("title", "").strip(),
                "date": request.form.get("date", "").strip() or None,
                "character": request.form.get("character", "").strip(),
                "category": request.form.get("category", "").strip(),
                "entry_type": request.form.get("entry_type", "personal memory").strip(),
                "description": request.form.get("description", "").strip(),
                "source": request.form.get("source", "personal").strip(),
            }
            # Preserve existing values for anything left blank.
            final = {
                "title": raw["title"] or m.title,
                "date": raw["date"] if raw["date"] is not None else m.date,
                "character": raw["character"] or m.character,
                "category": raw["category"] or m.category,
                "entry_type": raw["entry_type"] or m.entry_type,
                "description": raw["description"] if raw["description"] is not None else m.description,
                "source": raw["source"] or m.source,
            }
            try:
                updated = service.update_milestone(milestone_id, final)
                flash(f"Updated milestone {updated.id}", "success")
                return redirect(url_for("timeline_detail", milestone_id=updated.id))
            except ValidationError as exc:
                flash(str(exc), "error")
            except StorageError as exc:
                flash(str(exc), "error")
        characters = service.known_characters()
        entry_types = list(ENTRY_TYPES_FOR_WEB)
        categories = sorted({m2.category for m2 in service.storage.list_milestones()})
        return render_template(
            "timeline_edit.html",
            m=m,
            characters=characters,
            entry_types=entry_types,
            categories=categories,
        )

    @app.route("/timeline/delete/<milestone_id>", methods=["POST"])
    def timeline_delete(milestone_id):
        m = service.get_milestone(milestone_id)
        if m is None:
            abort(404)
        try:
            removed = service.delete_milestone(milestone_id)
            flash(f"Deleted milestone {removed.id}: {removed.title}", "success")
        except StorageError as exc:
            flash(str(exc), "error")
        return redirect(url_for("timeline"))

    # -- characters ---------------------------------------------------- #
    @app.route("/characters")
    def characters():
        chars = service.known_characters()
        return render_template("characters.html", characters=chars)

    @app.route("/characters/<name>")
    def character_detail(name):
        chars = service.known_characters()
        if name not in chars:
            abort(404)
        info = chars[name]
        assoc = [m for m in service.list_milestones() if m.character == name]
        return render_template(
            "character_detail.html",
            name=name,
            info=info,
            milestones=assoc,
        )

    # -- PLA memories -------------------------------------------------- #
    @app.route("/pla")
    def pla():
        trio = ["Pure Vanilla Cookie", "White Lily Cookie", "Abinav"]
        chars = service.known_characters()
        sections = []
        for name in trio:
            info = chars.get(name, {})
            assoc = [m for m in service.list_milestones() if m.character == name]
            sections.append({"name": name, "info": info, "milestones": assoc})
        return render_template("pla.html", sections=sections)

    # -- memories / tribute garden ------------------------------------- #
    @app.route("/memories", methods=["GET", "POST"])
    def memories():
        if request.method == "POST":
            message = request.form.get("message", "").strip()
            name = request.form.get("name", "").strip() or "Visitor"
            if not message:
                flash("A message is required.", "error")
            elif len(message) > 500:
                flash("Message is too long (max 500 characters).", "error")
            else:
                messages = session.setdefault("garden_messages", [])
                messages.append(
                    {
                        "name": name,
                        "message": message,
                        "at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
                    }
                )
                session.modified = True
                flash("Your memory has been offered to the garden.", "success")
                return redirect(url_for("memories"))
        messages = session.get("garden_messages", [])
        flower_count = len(session.get("flowers_offered", set()))
        return render_template("memories.html", messages=messages, flower_count=flower_count)

    @app.route("/memories/offer-flower", methods=["POST"])
    def offer_flower():
        # Session-based counter; each click adds one flower (max one per session per user tracked by id).
        offered = session.setdefault("flowers_offered", set())
        token = str(uuid.uuid4())
        offered.add(token)
        session.modified = True
        count = len(offered)
        if request.is_json:
            return {"flowers": count}
        flash(f"A flower has been offered. Total this session: {count}", "success")
        return redirect(url_for("memories"))

    # -- error pages --------------------------------------------------- #
    @app.errorhandler(404)
    def _not_found(e):
        return render_template("error.html", code=404, title="Not Found", message="That memory could not be found."), 404

    @app.errorhandler(403)
    def _forbidden(e):
        return render_template("error.html", code=403, title="Forbidden", message="Request could not be verified."), 403

    @app.errorhandler(500)
    def _server_error(e):
        return render_template("error.html", code=500, title="Server Error", message="Something went wrong."), 500

    return app


ENTRY_TYPES_FOR_WEB = ("official fact", "personal memory", "fan interpretation")
