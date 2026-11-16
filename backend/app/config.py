"""Everlasting Bloom Studio — environment-based configuration.

Never store real secrets here. Copy .env.example to .env and fill in
values locally. The .env file is gitignored and must never be committed.
"""

from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # everlasting-bloom-studio/
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = BASE_DIR / "uploads"


def _env(key: str, default: str | None = None) -> str | None:
    return os.environ.get(key, default)


class Config:
    """Base configuration. All values overridable via environment variables."""

    SECRET_KEY = _env("SECRET_KEY", "dev-secret-change-me")
    WTF_CSRF_ENABLED = True

    # Flask
    FLASK_APP = _env("FLASK_APP", "app:create_app")
    FLASK_ENV = _env("FLASK_ENV", "development")
    FLASK_DEBUG = _env("FLASK_DEBUG", "false").lower() == "true"
    FLASK_HOST = _env("FLASK_HOST", "127.0.0.1")
    FLASK_PORT = int(_env("FLASK_PORT", "5000") or "5000")

    # SQLite database
    DATABASE_URL = _env(
        "DATABASE_URL", f"sqlite:///{DATA_DIR / 'everlasting_bloom.db'}"
    )
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads
    MAX_CONTENT_LENGTH = int(_env("MAX_CONTENT_LENGTH", "16777216"))  # 16 MB
    UPLOAD_FOLDER = str(UPLOADS_DIR)

    # Sessions / auth
    SESSION_COOKIE_NAME = "everlasting_bloom_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME_SECONDS = int(
        _env("PERMANENT_SESSION_LIFETIME_SECONDS", "86400") or "86400"
    )

    # Hermes Agent integration (real interfaces only — never simulated)
    HERMES_CLI = _env("HERMES_CLI", "hermes")
    HERMES_PROFILE = _env("HERMES_PROFILE", "lilymogra-studio")
    HERMES_HOME = _env("HERMES_HOME", str(Path.home() / ".hermes"))
    HERMES_SERVE_PORT = int(_env("HERMES_SERVE_PORT", "9119") or "9119")
    HERMES_SERVE_HOST = _env("HERMES_SERVE_HOST", "127.0.0.1")

    # Security: safe command allowlist for the Hermes terminal page.
    # Only these `hermes` subcommands may be invoked from the browser.
    HERMES_ALLOWED_COMMANDS = [
        "status",
        "doctor",
        "skills",
        "memory",
        "sessions",
        "logs",
        "config",
        "security",
        "profile",
    ]


class DevelopmentConfig(Config):
    FLASK_DEBUG = True


class TestingConfig(Config):
    FLASK_DEBUG = False
    DATABASE_URL = "sqlite:///:memory:"
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    FLASK_DEBUG = False
    SESSION_COOKIE_SECURE = True


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config() -> Config:
    name = _env("FLASK_ENV", "development")
    return config_by_name.get(name, DevelopmentConfig)
