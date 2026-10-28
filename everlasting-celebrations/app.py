"""
CookieVerse: Everlasting Celebrations
-------------------------------------
An unofficial Cookie Run fan project celebrating game anniversaries,
legendary characters, fan-made events, and community memories.

NOT affiliated with or endorsed by Devsisters Corporation.
All Cookie Run trademarks and intellectual property belong to their owners.
"""

import os
import secrets
import sqlite3
from datetime import datetime, timedelta
from flask import (
    Flask, render_template, request, jsonify, session,
    g, abort, redirect, url_for, flash
)

app = Flask(__name__, instance_relative_config=True)

# ---- Configuration ----
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
app.config["DATABASE"] = os.path.join(app.instance_path, "celebrations.db")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB upload cap
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# ---- Anniversary reference dates (fan-maintained, clearly labelled) ----
# Cookie Run: OvenBreak launched globally on October 27, 2016.
# The 10th anniversary is October 27, 2026. We present this as a
# community reference date — never as an official Devsisters announcement.
OVENBREAK_LAUNCH = datetime(2016, 10, 27)
TENTH_ANNIVERSARY = datetime(2026, 10, 27)


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create tables if they don't exist."""
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL DEFAULT '',
        content TEXT NOT NULL,
        favorite_cookie TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS fan_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        celebration_date TEXT,
        theme TEXT NOT NULL DEFAULT 'golden',
        preset TEXT NOT NULL DEFAULT 'original',
        is_unofficial INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """)
    db.commit()


def seed_defaults():
    """Insert default settings and seed data if tables are empty."""
    db = get_db()

    # Default settings
    defaults = {
        "theme": "light",
        "reduced_motion": "false",
        "sound_enabled": "true",
    }
    for key, value in defaults.items():
        existing = db.execute(
            "SELECT 1 FROM settings WHERE key = ?", (key,)
        ).fetchone()
        if not existing:
            db.execute(
                "INSERT INTO settings (key, value) VALUES (?, ?)", (key, value)
            )
    db.commit()

    # Seed fan-event presets only if the table is empty
    count = db.execute("SELECT COUNT(*) AS c FROM fan_events").fetchone()["c"]
    if count == 0:
        presets = [
            {
                "title": "OvenBreak Decade Celebration",
                "description": "A community celebration of ten years of Cookie Run: OvenBreak running, jelly, and friendship.",
                "celebration_date": "2026-10-27",
                "theme": "golden",
                "preset": "ovenbreak",
            },
            {
                "title": "Kingdom Anniversary Gathering",
                "description": "Fan-organized celebration for Cookie Run: Kingdom anniversaries and kingdom-building milestones.",
                "celebration_date": None,
                "theme": "rainbow",
                "preset": "kingdom",
            },
            {
                "title": "Original Fan Anniversary",
                "description": "Your very own custom Cookie Run fan celebration. Choose your date, theme, and story.",
                "celebration_date": None,
                "theme": "cream",
                "preset": "original",
            },
        ]
        for ev in presets:
            db.execute(
                """INSERT INTO fan_events
                   (title, description, celebration_date, theme, preset, is_unofficial, created_at)
                   VALUES (?, ?, ?, ?, ?, 1, ?)""",
                (
                    ev["title"], ev["description"], ev["celebration_date"],
                    ev["theme"], ev["preset"], datetime.utcnow().isoformat(),
                ),
            )
        db.commit()


@app.route("/init")
def initialize():
    """Dev helper: (re)initialize the database and seed defaults."""
    with app.app_context():
        init_db()
        seed_defaults()
    return jsonify({"status": "ok", "message": "Database initialized."})


# ---------------------------------------------------------------------------
# CSRF protection (simple, session-based)
# ---------------------------------------------------------------------------
def generate_csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(32)
    return session["_csrf_token"]


app.jinja_env.globals["csrf_token"] = generate_csrf_token


def validate_csrf():
    """Validate CSRF token for state-changing requests."""
    if request.method in ("POST", "PUT", "DELETE", "PATCH"):
        token = (
            request.form.get("csrf_token")
            or request.headers.get("X-CSRFToken")
            or (request.get_json(silent=True) or {}).get("csrf_token")
        )
        if not token or token != session.get("_csrf_token"):
            abort(403, description="Invalid or missing CSRF token.")


@app.before_request
def _csrf_protect():
    validate_csrf()


# ---------------------------------------------------------------------------
# Context processor: inject settings + anniversary info into all templates
# ---------------------------------------------------------------------------
@app.context_processor
def inject_globals():
    db = get_db()
    settings = {row["key"]: row["value"] for row in db.execute("SELECT key, value FROM settings")}
    return {
        "site_name": "CookieVerse",
        "site_tagline": "Every Legend. Every Memory. Every Celebration.",
        "ovenbreak_launch": OVENBREAK_LAUNCH.strftime("%B %d, %Y"),
        "tenth_anniversary": TENTH_ANNIVERSARY.strftime("%B %d, %Y"),
        "settings": settings,
        "unofficial_label": (
            "Unofficial fan project — not affiliated with or endorsed by Devsisters."
        ),
    }


# ---------------------------------------------------------------------------
# Routes — Pages
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/timeline")
def timeline():
    return render_template("timeline.html")


@app.route("/memories")
def memories_page():
    return render_template("memories.html")


@app.route("/fan-events")
def fan_events_page():
    return render_template("fan_events.html")


@app.route("/countdown")
def countdown_page():
    return render_template("countdown.html")


@app.route("/settings")
def settings_page():
    return render_template("settings.html")


@app.route("/mini-game")
def mini_game_page():
    return render_template("mini_game.html")


# ---------------------------------------------------------------------------
# API — Memories (Memory Oven)
# ---------------------------------------------------------------------------
@app.route("/api/memories", methods=["GET"])
def api_list_memories():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM memories ORDER BY created_at DESC"
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/memories", methods=["POST"])
def api_create_memory():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()[:100]
    content = (data.get("content") or "").strip()
    favorite_cookie = (data.get("favorite_cookie") or "").strip()[:50]

    if not content:
        return jsonify({"error": "Memory content is required."}), 400
    if len(content) > 2000:
        return jsonify({"error": "Memory content is too long (max 2000 characters)."}), 400

    db = get_db()
    cur = db.execute(
        """INSERT INTO memories (title, content, favorite_cookie, created_at)
           VALUES (?, ?, ?, ?)""",
        (title, content, favorite_cookie, datetime.utcnow().isoformat()),
    )
    db.commit()
    new_id = cur.lastrowid
    row = db.execute("SELECT * FROM memories WHERE id = ?", (new_id,)).fetchone()
    return jsonify(dict(row)), 201


@app.route("/api/memories/<int:memory_id>", methods=["DELETE"])
def api_delete_memory(memory_id):
    db = get_db()
    row = db.execute("SELECT * FROM memories WHERE id = ?", (memory_id,)).fetchone()
    if not row:
        return jsonify({"error": "Memory not found."}), 404
    db.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
    db.commit()
    return jsonify({"success": True, "id": memory_id})


# ---------------------------------------------------------------------------
# API — Fan Events (Fan Event Studio)
# ---------------------------------------------------------------------------
@app.route("/api/fan-events", methods=["GET"])
def api_list_fan_events():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM fan_events ORDER BY created_at DESC"
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/fan-events", methods=["POST"])
def api_create_fan_event():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()[:100]
    description = (data.get("description") or "").strip()
    celebration_date = (data.get("celebration_date") or "").strip() or None
    theme = (data.get("theme") or "golden").strip()[:30]
    preset = (data.get("preset") or "original").strip()[:30]

    if not title:
        return jsonify({"error": "Event title is required."}), 400
    if not description:
        return jsonify({"error": "Event description is required."}), 400

    # Validate date if provided
    if celebration_date:
        try:
            datetime.strptime(celebration_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid celebration date format (use YYYY-MM-DD)."}), 400

    db = get_db()
    cur = db.execute(
        """INSERT INTO fan_events
           (title, description, celebration_date, theme, preset, is_unofficial, created_at)
           VALUES (?, ?, ?, ?, ?, 1, ?)""",
        (
            title, description, celebration_date, theme, preset,
            datetime.utcnow().isoformat(),
        ),
    )
    db.commit()
    new_id = cur.lastrowid
    row = db.execute("SELECT * FROM fan_events WHERE id = ?", (new_id,)).fetchone()
    return jsonify(dict(row)), 201


@app.route("/api/fan-events/<int:event_id>", methods=["DELETE"])
def api_delete_fan_event(event_id):
    db = get_db()
    row = db.execute("SELECT * FROM fan_events WHERE id = ?", (event_id,)).fetchone()
    if not row:
        return jsonify({"error": "Fan event not found."}), 404
    # Only allow deletion of user-created events? For simplicity: allow all.
    db.execute("DELETE FROM fan_events WHERE id = ?", (event_id,))
    db.commit()
    return jsonify({"success": True, "id": event_id})


# ---------------------------------------------------------------------------
# API — Countdown (user-selectable date)
# ---------------------------------------------------------------------------
@app.route("/api/countdown", methods=["POST"])
def api_calculate_countdown():
    data = request.get_json(silent=True) or {}
    target = data.get("target_date", "").strip()

    if not target:
        return jsonify({"error": "A target date is required."}), 400

    try:
        target_dt = datetime.strptime(target, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    now = datetime.utcnow()
    diff = target_dt - now

    result = {
        "target_date": target,
        "target_datetime": target_dt.isoformat(),
    }

    if diff.days < 0:
        result["status"] = "past"
        result["message"] = f"That celebration date ({target}) has already passed."
        result["days_passed"] = abs(diff.days)
    elif diff.days == 0 and diff.seconds == 0:
        result["status"] = "today"
        result["message"] = "It's celebration day today!"
    else:
        result["status"] = "future"
        total_seconds = int(diff.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        result["days"] = days
        result["hours"] = hours
        result["minutes"] = minutes
        result["seconds"] = seconds
        result["message"] = (
            f"{days} day(s), {hours} hour(s), {minute if False else minutes} minute(s), "
            f"{seconds} second(s) until {target}."
        )

    return jsonify(result)


@app.route("/api/countdown/ovenbreak", methods=["GET"])
def api_ovenbreak_countdown():
    """Reference countdown to the community-noted OvenBreak 10th anniversary."""
    now = datetime.utcnow()
    diff = TENTH_ANNIVERSARY - now
    result = {
        "event": "Cookie Run: OvenBreak 10th Anniversary (community reference)",
        "reference_date": "October 27, 2026",
        "label": "fan-maintained reference date — not an official Devsisters announcement",
    }
    if diff.days < 0:
        result["status"] = "passed"
        result["message"] = "The 10th anniversary reference date has passed."
    elif diff.days == 0:
        result["status"] = "today"
        result["message"] = "Happy 10th Anniversary reference day!"
    else:
        total_seconds = int(diff.total_seconds())
        result["days"] = total_seconds // 86400
        result["hours"] = (total_seconds % 86400) // 3600
        result["minutes"] = (total_seconds % 3600) // 60
        result["seconds"] = total_seconds % 60
        result["status"] = "future"
    return jsonify(result)


# ---------------------------------------------------------------------------
# API — Settings
# ---------------------------------------------------------------------------
@app.route("/api/settings", methods=["GET"])
def api_get_settings():
    db = get_db()
    rows = db.execute("SELECT key, value FROM settings").fetchall()
    return jsonify({r["key"]: r["value"] for r in rows})


@app.route("/api/settings", methods=["POST"])
def api_update_settings():
    data = request.get_json(silent=True) or {}
    allowed = {"theme", "reduced_motion", "sound_enabled"}
    db = get_db()
    for key, value in data.items():
        if key not in allowed:
            continue
        db.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, str(value)),
        )
    db.commit()
    return jsonify({"success": True})


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------
@app.errorhandler(403)
def csrf_error(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": str(e.description or "CSRF validation failed.")}), 403
    return render_template("error.html", code=403, message=str(e.description or "Forbidden")), 403


@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Not found."}), 404
    return render_template("error.html", code=404, message="Page not found."), 404


@app.errorhandler(500)
def server_error(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Internal server error."}), 500
    return render_template("error.html", code=500, message="Something went wrong."), 500


if __name__ == "__main__":
    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    with app.app_context():
        init_db()
        seed_defaults()
    # NEVER run debug=True in production.
    app.run(host="0.0.0.0", port=5000, debug=False)
