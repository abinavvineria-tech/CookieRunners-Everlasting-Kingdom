"""Everlasting Bloom Studio — WSGI entry point.

Usage (from project root):
  source .venv/bin/activate
  flask --app backend.app:create_app run --debug

Or with gunicorn:
  gunicorn backend.app:create_app --factory
"""

from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
