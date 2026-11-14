"""Everlasting Bloom Studio — Flask application factory.

Shared backend serving three pillars:
  - Everlasting Bloom (fan universe)     -> /api/universe, /pages/*
  - Everbloom Studio (creative workspace) -> /api/studio, /studio/*
  - Hermes WebUI (agent control center)  -> /api/hermes, /hermes/*

Persistence: SQLite via Flask-SQLAlchemy.
Configuration: env-based (see backend/app/config.py).
"""

from __future__ import annotations

import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from .config import get_config, DATA_DIR, UPLOADS_DIR
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Single shared extension instances (models import `db` from here).
# SQLAlchemy uses Base as the declarative model class.
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_object=None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder=None, static_url_path=None)

    if config_object is None:
        config_object = get_config()
    app.config.from_object(config_object)

    # Ensure data / uploads directories exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "api.auth_login"
    login_manager.session_protection = "strong"

    # Flask-Login user loader
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    from .routes import api_bp, pages_bp

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(pages_bp)

    # Health check
    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "service": "everlasting-bloom-studio",
            "version": "0.1.0",
        }, 200

    @app.get("/api/health")
    def api_health():
        return {
            "status": "ok",
            "service": "everlasting-bloom-studio-backend",
            "version": "0.1.0",
        }, 200

    # Error handlers (JSON for API routes)
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not_found", "message": str(e)}), 404

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return jsonify({"error": "internal_error", "message": "server error"}), 500

    return app
