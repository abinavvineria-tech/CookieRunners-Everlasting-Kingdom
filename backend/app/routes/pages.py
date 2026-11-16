"""Everlasting Bloom Studio — page routes (serves the React SPA).

The frontend is a single-page app. Flask renders index.html for all
non-API routes so that client-side routing works. Static assets are served
from the built frontend dist/ directory when available; in development the
Vite dev server is used via the frontend proxy.
"""

from __future__ import annotations

import os
from flask import Blueprint, send_from_directory, abort

pages_bp = Blueprint("pages", __name__)

# Resolve the frontend dist directory: <root>/frontend/dist
FRONTEND_DIST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "frontend", "dist",
)


@pages_bp.route("/", defaults={"path": ""})
@pages_bp.route("/<path:path>")
def spa(path: str):
    """Serve the SPA index.html for client-side routes, falling back to
    static assets when the requested path matches a real file."""
    if path and os.path.exists(os.path.join(FRONTEND_DIST, path)):
        return send_from_directory(FRONTEND_DIST, path)

    index_path = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(FRONTEND_DIST, "index.html")

    abort(404, description="Frontend not built yet. Run `npm run build` in frontend/ or start the Vite dev server.")


@pages_bp.route("/uploads/<path:filename>")
def uploaded_file(filename):
    """Serve uploaded gallery assets."""
    from ..config import UPLOADS_DIR
    return send_from_directory(str(UPLOADS_DIR), filename)
