"""Flask backend for Champions League Countdown Nexus.

Serves the countdown frontend and exposes event data as JSON.
Event configuration lives in data/events.json so it can be updated
without touching code.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, jsonify, render_template, request

from config import (
    DATA_DIR,
    DEFAULT_EVENT,
    EVENTS_FILE,
    EVENT_TZ,
    PERSIST_EVENTS,
)

IST = EVENT_TZ  # Asia/Kolkata alias for clarity


def _load_events() -> dict:
    """Load event configuration from the JSON file, falling back to defaults."""
    try:
        with open(EVENTS_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            return dict(DEFAULT_EVENT)
        merged = dict(DEFAULT_EVENT)
        merged.update(data)
        return merged
    except FileNotFoundError:
        return dict(DEFAULT_EVENT)
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_EVENT)


def _save_events(event: dict) -> None:
    """Persist event configuration to the JSON file (optional)."""
    if not PERSIST_EVENTS:
        return
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(EVENTS_FILE, "w", encoding="utf-8") as fh:
        json.dump(event, fh, indent=2, ensure_ascii=False)


def _parse_event_datetime(event: dict) -> datetime:
    """Parse the event date/time into a timezone-aware datetime (Asia/Kolkata).

    Never hardcodes the countdown value — the target is always derived
    from the configured event date/time/timezone.
    """
    date_str = event.get("date", DEFAULT_EVENT["date"])
    time_str = event.get("time", DEFAULT_EVENT["time"])
    tz_name = event.get("timezone", DEFAULT_EVENT["timezone"])

    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz = IST

    naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    return naive.replace(tzinfo=tz)


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "static"),
    )
    app.config["JSON_SORT_KEYS"] = False
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/event", methods=["GET"])
    def api_event():
        """Return the current event configuration and computed countdown state."""
        event = _load_events()
        target = _parse_event_datetime(event)
        now = datetime.now(tz=IST)
        diff_seconds = int((target - now).total_seconds())

        launched = diff_seconds <= 0

        # Break down the remaining time into days/hours/minutes/seconds.
        remaining = max(diff_seconds, 0)
        days = remaining // (24 * 3600)
        remaining %= 24 * 3600
        hours = remaining // 3600
        remaining %= 3600
        minutes = remaining // 60
        seconds = remaining % 60

        return jsonify(
            {
                "event": event,
                "target_iso": target.isoformat(),
                "target_label": target.strftime("%d %B %Y, %I:%M %p %Z"),
                "timezone": str(IST),
                "now_iso": now.isoformat(),
                "diff_seconds": diff_seconds,
                "launched": launched,
                "countdown": {
                    "days": days,
                    "hours": hours,
                    "minutes": minutes,
                    "seconds": seconds,
                },
                "status": "launched" if launched else "counting_down",
            }
        )

    @app.route("/api/event", methods=["POST"])
    def api_update_event():
        """Validate and persist updated event configuration.

        Validates date, time, and timezone before saving. Returns 400 on
        invalid input.
        """
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        payload = request.get_json(silent=True) or {}

        date_str = payload.get("date", "").strip()
        time_str = payload.get("time", "").strip()
        tz_name = payload.get("timezone", "Asia/Kolkata").strip()

        # Validate date.
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid date. Use YYYY-MM-DD."}), 400

        # Validate time.
        try:
            datetime.strptime(time_str, "%H:%M")
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid time. Use HH:MM."}), 400

        # Validate timezone.
        try:
            ZoneInfo(tz_name)
        except Exception:
            return jsonify({"error": "Invalid timezone."}), 400

        event = {
            "name": (payload.get("name") or DEFAULT_EVENT["name"]).strip(),
            "date": date_str,
            "time": time_str,
            "timezone": tz_name,
            "kickoff_label": (payload.get("kickoff_label") or "").strip()
            or f"{time_str} {tz_name.split('/')[-1]}",
            "description": (payload.get("description") or DEFAULT_EVENT["description"]).strip(),
            "unofficial_note": DEFAULT_EVENT["unofficial_note"],
        }

        _save_events(event)
        return jsonify({"status": "ok", "event": event}), 200

    @app.route("/api/health")
    def api_health():
        return jsonify({"status": "ok", "project": "Champions League Countdown Nexus"})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "not found"}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "internal server error"}), 500

    return app


# Module-level app instance for `flask --app` and gunicorn/uWSGI.
app = create_app()

if __name__ == "__main__":
    # Bind to all interfaces so it's reachable from Android devices on LAN.
    app.run(
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("DEBUG", "true").lower() == "true",
    )
