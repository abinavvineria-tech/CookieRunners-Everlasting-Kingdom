"""EverLink SSH Flask web application.

Local-only development server bound to 127.0.0.1 by default. All SSH launches
use safe subprocess argument arrays. CSRF-protected state-changing routes.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from . import __version__, APP_TITLE
from . import config as cfg
from . import database as db
from .security import (
    ValidationError,
    generate_csrf_token,
    validate_hostname,
    validate_identity_file,
    validate_port,
    validate_profile_name,
    validate_username,
)
from .ssh_manager import (
    build_ssh_command,
    connect,
    keygen,
    list_public_keys,
    ssh_available,
    tcp_reachability,
)

APP_SECRET_ENV = "EVERLINK_SECRET_KEY"


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = os.environ.get(APP_SECRET_ENV) or os.urandom(24)
    app.config["MAX_CONTENT_LENGTH"] = 1_048_576  # 1 MB request limit
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = False  # localhost-only dev server

    # Ensure the data dir exists before first request.
    cfg.app_data_dir().mkdir(parents=True, exist_ok=True)
    cfg.app_config_dir().mkdir(parents=True, exist_ok=True)
    db.init_db()

    @app.before_request
    def ensure_csrf_token():
        if "csrf_token" not in session:
            session["csrf_token"] = generate_csrf_token()

    def csrf_token() -> str:
        return session.get("csrf_token") or generate_csrf_token()

    def validate_csrf() -> bool:
        token = session.get("csrf_token")
        provided = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token")
        if not token or not provided:
            return False
        return secrets_compare(token, provided)

    def secrets_compare(a: str, b: str) -> bool:
        import secrets as _secrets

        return _secrets.compare_digest(a or "", b or "")

    app.jinja_env.globals["csrf_token"] = csrf_token
    app.jinja_env.globals["csrf_field"] = (
        lambda: f'<input type="hidden" name="csrf_token" value="{csrf_token()}">'
    )
    app.jinja_env.globals["settings"] = cfg.load_settings
    app.jinja_env.globals["version"] = lambda: __version__

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def flash_error(message: str) -> None:
        flash(message, "error")

    def flash_success(message: str) -> None:
        flash(message, "success")

    # ------------------------------------------------------------------ #
    # Routes
    # ------------------------------------------------------------------ #
    @app.route("/")
    def dashboard():
        settings = cfg.load_settings()
        conn = db.get_connection()
        try:
            hosts = db.list_hosts(conn)
            attempts = db.recent_attempts(conn, limit=8)
        finally:
            conn.close()
        return render_template(
            "dashboard.html",
            hosts=hosts,
            attempts=attempts,
            ssh_available=ssh_available(),
            host_count=len(hosts),
        )

    @app.route("/hosts")
    def hosts():
        search = request.args.get("search", "").strip() or None
        conn = db.get_connection()
        try:
            hosts = db.list_hosts(conn, search=search)
        finally:
            conn.close()
        return render_template("hosts.html", hosts=hosts, search=search or "")

    @app.route("/hosts/add", methods=["GET", "POST"])
    def host_add():
        if request.method == "POST":
            if not validate_csrf():
                abort(403)
            try:
                name = validate_profile_name(request.form.get("name", ""))
                hostname = validate_hostname(request.form.get("hostname", ""))
                username = validate_username(request.form.get("username", ""))
                port = validate_port(request.form.get("port", cfg.DEFAULT_SSH_PORT))
                identity_file = validate_identity_file(request.form.get("identity_file") or None)
            except ValidationError as exc:
                flash_error(str(exc))
                return render_template("host_form.html", mode="add", form=request.form), 400

            conn = db.get_connection()
            try:
                if db.get_host(conn, name) is not None:
                    flash_error(f"Profile '{name}' already exists.")
                    return render_template("host_form.html", mode="add", form=request.form), 400
                db.add_host(conn, name, hostname, username, port, identity_file)
                flash_success(f"Added profile '{name}'.")
                return redirect(url_for("hosts"))
            finally:
                conn.close()
        return render_template("host_form.html", mode="add", form={})

    @app.route("/hosts/<int:host_id>/edit", methods=["GET", "POST"])
    def host_edit(host_id):
        conn = db.get_connection()
        try:
            row = db.get_host_by_id(conn, host_id)
            if row is None:
                abort(404)
            if request.method == "POST":
                if not validate_csrf():
                    abort(403)
                try:
                    name = validate_profile_name(request.form.get("name", ""))
                    hostname = validate_hostname(request.form.get("hostname", ""))
                    username = validate_username(request.form.get("username", ""))
                    port = validate_port(request.form.get("port", cfg.DEFAULT_SSH_PORT))
                    identity_file = validate_identity_file(request.form.get("identity_file") or None)
                except ValidationError as exc:
                    flash_error(str(exc))
                    form = dict(row)
                    form.update(request.form)
                    return render_template("host_form.html", mode="edit", host=row, form=form), 400
                # Name uniqueness (excluding self)
                existing = db.get_host(conn, name)
                if existing is not None and existing["id"] != host_id:
                    flash_error(f"Profile '{name}' already exists.")
                    form = dict(row)
                    form.update(request.form)
                    return render_template("host_form.html", mode="edit", host=row, form=form), 400
                db.update_host(
                    conn,
                    host_id,
                    name=name,
                    hostname=hostname,
                    username=username,
                    port=port,
                    identity_file=identity_file,
                )
                flash_success(f"Updated profile '{name}'.")
                return redirect(url_for("hosts"))
        finally:
            conn.close()
        form = dict(row)
        return render_template("host_form.html", mode="edit", host=row, form=form)

    @app.route("/hosts/<int:host_id>/delete", methods=["POST"])
    def host_delete(host_id):
        if not validate_csrf():
            abort(403)
        conn = db.get_connection()
        try:
            row = db.get_host_by_id(conn, host_id)
            if row is None:
                abort(404)
            db.delete_host(conn, host_id)
            flash_success(f"Deleted profile '{row['name']}'.")
        finally:
            conn.close()
        return redirect(url_for("hosts"))

    @app.route("/hosts/<int:host_id>/connect", methods=["POST"])
    def host_connect(host_id):
        if not validate_csrf():
            abort(403)
        conn = db.get_connection()
        try:
            row = db.get_host_by_id(conn, host_id)
            if row is None:
                abort(404)
            profile = dict(row)
        finally:
            conn.close()

        if not ssh_available():
            flash_error("OpenSSH client is not installed on this device.")
            return redirect(url_for("hosts"))

        target = f"{profile['username']}@{profile['hostname']}:{profile.get('port', 22)}"
        try:
            rc = connect(profile)
            if rc == 0:
                flash_success(f"Session to {target} ended normally.")
            else:
                flash_error(f"Session to {target} ended with code {rc}.")
        except Exception as exc:  # noqa: BLE001
            flash_error(f"Failed to launch SSH: {exc}")
        return redirect(url_for("hosts"))

    @app.route("/keys")
    def keys():
        keys = list_public_keys()
        return render_template("keys.html", keys=keys)

    @app.route("/keys/generate", methods=["POST"])
    def keys_generate():
        if not validate_csrf():
            abort(403)
        key_type = request.form.get("key_type", "ed25519")
        comment = request.form.get("comment", "")
        passphrase = request.form.get("passphrase", "")
        try:
            path = validate_identity_file(request.form.get("path") or None)
        except ValidationError as exc:
            flash_error(str(exc))
            return redirect(url_for("keys"))
        rc, out, err = keygen(key_type=key_type, path=path, comment=comment, passphrase=passphrase)
        if rc == 0:
            flash_success(f"Key generated at {path or os.path.expanduser('~/.ssh/id_ed25519')}")
        else:
            flash_error(f"Key generation failed: {err.strip() or out.strip()}")
        return redirect(url_for("keys"))

    @app.route("/diagnostics")
    def diagnostics():
        from .diagnostics import run_doctor

        info = run_doctor()
        reachable = None
        reach_message = None
        if request.args.get("check_host"):
            host = request.args.get("check_host", "").strip()
            port = int(request.args.get("check_port", 22))
            try:
                reachable, reach_message = tcp_reachability(host, port, timeout=3.0)
            except Exception as exc:  # noqa: BLE001
                reachable = None
                reach_message = str(exc)
        return render_template("diagnostics.html", info=info, reachable=reachable, reach_message=reach_message)

    @app.route("/settings", methods=["GET", "POST"])
    def settings():
        if request.method == "POST":
            if not validate_csrf():
                abort(403)
            new_settings = dict(cfg.load_settings())
            try:
                new_settings["default_ssh_port"] = validate_port(request.form.get("default_ssh_port", 22))
                new_settings["web_port"] = validate_port(request.form.get("web_port", cfg.DEFAULT_WEB_PORT))
                new_settings["theme"] = request.form.get("theme", "midnight").strip() or "midnight"
                new_settings["terminal_preference"] = request.form.get("terminal_preference", "native")
            except ValidationError as exc:
                flash_error(str(exc))
                return render_template("settings.html", settings=new_settings), 400
            cfg.save_settings(new_settings)
            flash_success("Settings saved.")
            return redirect(url_for("settings"))
        return render_template("settings.html", settings=cfg.load_settings())

    @app.route("/api/hosts")
    def api_hosts():
        conn = db.get_connection()
        try:
            hosts = db.list_hosts(conn)
        finally:
            conn.close()
        return jsonify([dict(h) for h in hosts])

    @app.route("/api/connect/<int:host_id>", methods=["POST"])
    def api_connect(host_id):
        if not validate_csrf():
            return jsonify({"error": "CSRF token missing"}), 403
        if not ssh_available():
            return jsonify({"error": "OpenSSH not available"}), 503
        conn = db.get_connection()
        try:
            row = db.get_host_by_id(conn, host_id)
            if row is None:
                return jsonify({"error": "not found"}), 404
            profile = dict(row)
        finally:
            conn.close()
        args = build_ssh_command(
            user=profile.get("username"),
            host=profile["hostname"],
            port=int(profile.get("port", 22)),
            identity_file=profile.get("identity_file"),
        )
        return jsonify({"command": " ".join(args), "argv": args})

    return app
