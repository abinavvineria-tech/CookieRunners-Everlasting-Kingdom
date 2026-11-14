"""Everlasting Bloom Studio — SQLAlchemy models and shared db instance.

Three pillars share this database:
  - Everlasting Bloom (fan universe): characters, timeline, memories, gallery
  - Everbloom Studio (creative workspace): studio projects + assets
  - Hermes WebUI: integration status only (agent operational data stays in ~/.hermes)

Content-type flags keep game canon, personal memories, and fan fiction clearly
distinguished. No Hermes secrets, credentials, or agent state are stored here.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

# Import the single shared db instance from the application package.
# app/__init__.py defines db = SQLAlchemy(model_class=Base).
from .. import db
from flask_sqlalchemy import SQLAlchemy  # noqa: F401  (re-exported for convenience)
import enum as enum_mod

from sqlalchemy import String, Text, Integer, Boolean, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship


# ---------------------------------------------------------------------------
# Mixins
# ---------------------------------------------------------------------------

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True,
    )


# ---------------------------------------------------------------------------
# Users / auth (shared across pillars — studio admin only)
# ---------------------------------------------------------------------------

class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def set_password(self, plain: str) -> None:
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(plain)

    def check_password(self, plain: str) -> bool:
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, plain)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "is_admin": self.is_admin,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ---------------------------------------------------------------------------
# Pillar 1: Everlasting Bloom (fan universe)
# ---------------------------------------------------------------------------

class ContentType(str, enum_mod.Enum):
    CANON = "canon"
    PERSONAL = "personal"
    FAN_FICTION = "fan_fiction"


class Character(TimestampMixin, db.Model):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    display_name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_type: Mapped[str] = mapped_column(String(32), default=ContentType.CANON.value, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    is_ancient_hero: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_purelily: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    timeline_entries: Mapped[list["TimelineEntry"]] = relationship(
        back_populates="character", cascade="all, delete-orphan"
    )
    memories: Mapped[list["Memory"]] = relationship(
        back_populates="character", cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "content_type": self.content_type,
            "image_url": self.image_url,
            "is_ancient_hero": self.is_ancient_hero,
            "is_purelily": self.is_purelily,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class TimelineEntry(TimestampMixin, db.Model):
    __tablename__ = "timeline_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    event_date: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_type: Mapped[str] = mapped_column(String(32), default=ContentType.CANON.value, nullable=False)
    character_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("characters.id"), nullable=True
    )
    image_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    character = relationship("Character", back_populates="timeline_entries")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "event_date": self.event_date,
            "description": self.description,
            "content_type": self.content_type,
            "character_id": self.character_id,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Memory(TimestampMixin, db.Model):
    __tablename__ = "memories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_type: Mapped[str] = mapped_column(String(32), default=ContentType.PERSONAL.value, nullable=False)
    character_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("characters.id"), nullable=True
    )
    image_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    is_tribute: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    character = relationship("Character", back_populates="memories")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "content_type": self.content_type,
            "character_id": self.character_id,
            "image_url": self.image_url,
            "is_tribute": self.is_tribute,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class GalleryAsset(TimestampMixin, db.Model):
    __tablename__ = "gallery_assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(256), nullable=False)
    original_name: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    mime_type: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    alt_text: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    uploaded_by: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "filename": self.filename,
            "original_name": self.original_name,
            "mime_type": self.mime_type,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "alt_text": self.alt_text,
            "uploaded_by": self.uploaded_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# ---------------------------------------------------------------------------
# Pillar 2: Everbloom Studio (creative workspace)
# ---------------------------------------------------------------------------

class ProjectType(str, enum_mod.Enum):
    DOCUMENT = "document"
    TIMELINE = "timeline"
    MEMORY_CARD = "memory_card"
    LANDING_PAGE = "landing_page"
    GALLERY = "gallery"


# --- validation helpers for content-type / project-type (stored as String) ---
_CONTENT_TYPE_VALUES = {m.value for m in ContentType}
_PROJECT_TYPE_VALUES = {m.value for m in ProjectType}


def validate_content_type(value) -> str:
    if value is None:
        return ContentType.CANON.value
    v = value.value if hasattr(value, "value") else str(value)
    if v not in _CONTENT_TYPE_VALUES:
        raise ValueError(f"invalid content_type: {v}")
    return v


def validate_project_type(value) -> str:
    if value is None:
        return ProjectType.DOCUMENT.value
    v = value.value if hasattr(value, "value") else str(value)
    if v not in _PROJECT_TYPE_VALUES:
        raise ValueError(f"invalid project_type: {v}")
    return v

class StudioProject(TimestampMixin, db.Model):
    __tablename__ = "studio_projects"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    project_type: Mapped[str] = mapped_column(String(32), default=ProjectType.DOCUMENT.value, nullable=False)
    state_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_opened_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def to_dict(self) -> dict:
        import json
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "project_type": self.project_type,
            "state": json.loads(self.state_json) if self.state_json else None,
            "last_opened_at": self.last_opened_at.isoformat() if self.last_opened_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# ---------------------------------------------------------------------------
# Pillar 3: Hermes WebUI integration status (read-only mirror of health)
# ---------------------------------------------------------------------------

class HermesIntegrationStatus(TimestampMixin, db.Model):
    """A single row recording the last-known health of the Hermes bridge.

    Agent operational data (sessions, memories, skills, config) lives under
    ~/.hermes and is queried live via the `hermes` CLI — never duplicated here.
    """

    __tablename__ = "hermes_integration_status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hermes_cli_available: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    hermes_version: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    profile: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    last_check_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "hermes_cli_available": self.hermes_cli_available,
            "hermes_version": self.hermes_version,
            "profile": self.profile,
            "last_check_at": self.last_check_at.isoformat() if self.last_check_at else None,
            "last_error": self.last_error,
        }


__all__ = [
    "db",
    "Base",
    "TimestampMixin",
    "User",
    "Character",
    "TimelineEntry",
    "Memory",
    "GalleryAsset",
    "StudioProject",
    "HermesIntegrationStatus",
    "ContentType",
    "ProjectType",
]
