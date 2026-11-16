"""Everlasting Bloom Studio — database initialization & seed script.

Usage:
  source .venv/bin/activate
  python backend/init_db.py
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from backend.app import create_app, db
from backend.app.routes.api import ensure_default_admin


def main() -> int:
    app = create_app()
    with app.app_context():
        db.create_all()
        ensure_default_admin()
        print("Database initialized and default admin ensured.")
        print("  username: admin | password: admin (CHANGE BEFORE DEPLOYMENT)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
