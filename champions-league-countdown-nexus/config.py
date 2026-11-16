"""Configuration for Champions League Countdown Nexus.

Environment-variable driven. No plaintext secrets are committed here.
"""
from __future__ import annotations

import os
from zoneinfo import ZoneInfo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")

# Default event configuration (Asia/Kolkata / IST).
DEFAULT_EVENT = {
    "name": "Cookie Run Kingdom Champions League Welcome Night",
    "date": "2026-11-11",
    "time": "20:30",
    "timezone": "Asia/Kolkata",
    "kickoff_label": "8:30 PM IST",
    "description": (
        "The Cookie Run: Kingdom Champions League 2026 Welcome Night. "
        "One Kingdom. Multiple Servers. One Championship."
    ),
    "unofficial_note": "Unofficial fan project — not an official Devsisters website.",
}

# Timezone object for the event.
EVENT_TZ = ZoneInfo("Asia/Kolkata")

# Flask settings.
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
DEBUG = os.environ.get("DEBUG", "true").lower() == "true"
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5000"))

# Persistence toggle.
PERSIST_EVENTS = os.environ.get("PERSIST_EVENTS", "true").lower() == "true"
