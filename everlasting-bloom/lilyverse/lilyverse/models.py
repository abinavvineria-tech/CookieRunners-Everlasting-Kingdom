"""Shared data models and validation for LilyVerse.

Both the Flask website and the CLI operate on the same timeline records
through this module. Records are stored in a single JSON file.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


ENTRY_TYPES = ("official fact", "personal memory", "fan interpretation")

DEFAULT_CATEGORIES = (
    "franchise",
    "personal",
    "milestone",
    "project",
    "memory",
    "journey",
    "future",
)

DEFAULT_SOURCES = ("official", "personal", "fan")

CHARACTERS = {
    "White Lily Cookie": {
        "role": "Ancient Hero",
        "description": (
            "White Lily Cookie is an Ancient Hero of the Cookie Run Kingdom "
            "universe. Her story centers on truth, sacrifice, courage, "
            "friendship, and hope."
        ),
        "origin": "Official Cookie Run: Kingdom lore.",
    },
    "Pure Vanilla Cookie": {
        "role": "Ancient Hero",
        "description": (
            "Pure Vanilla Cookie is one of the Ancient Heroes, a wise and "
            "gentle guardian of the Cookie Kingdom."
        ),
        "origin": "Official Cookie Run: Kingdom lore.",
    },
    "Mogra Cookie": {
        "role": "Cookie",
        "description": (
            "Mogra Cookie is a beloved Cookie Run character known for her "
            "gentle, floral presence."
        ),
        "origin": "Official Cookie Run franchise.",
    },
    "Abinav": {
        "role": "Cookie Runner / creator",
        "description": (
            "Abinav (abinavzoey / CookieVerse Hermes) is a Cookie Runner from "
            "Tamil Nadu who joined Cookie Run: Kingdom on 2026-04-22 during the "
            "K-pop Demon Hunters collaboration."
        ),
        "origin": "Personal journey (not official game lore).",
    },
}

# Maximum length for free-text fields to keep the data store sane.
MAX_TITLE_LEN = 160
MAX_DESCRIPTION_LEN = 2000
MAX_SOURCE_LEN = 80
MAX_CATEGORY_LEN = 80


class LilyVerseError(Exception):
    """Base exception for LilyVerse data-layer errors."""


class ValidationError(LilyVerseError):
    """Raised when a record fails validation."""


class StorageError(LilyVerseError):
    """Raised when the data store cannot be read or written."""


@dataclass
class Milestone:
    """A single timeline milestone."""

    id: str
    title: str
    date: Optional[str]  # ISO YYYY-MM-DD or None (undated)
    character: str
    category: str
    entry_type: str
    description: str
    source: str
    created_at: str
    updated_at: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Milestone":
        return cls(
            id=str(data.get("id", "")),
            title=str(data.get("title", "")),
            date=data.get("date"),
            character=str(data.get("character", "")),
            category=str(data.get("category", "")),
            entry_type=str(data.get("entry_type", "personal memory")),
            description=str(data.get("description", "")),
            source=str(data.get("source", "personal")),
            created_at=str(data.get("created_at", "")),
            updated_at=str(data.get("updated_at", "")),
        )


@dataclass
class TimelineData:
    """The full contents of the JSON data store."""

    milestones: List[Milestone] = field(default_factory=list)
    version: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "milestones": [m.to_dict() for m in self.milestones],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TimelineData":
        milestones = [Milestone.from_dict(m) for m in data.get("milestones", [])]
        return cls(milestones=milestones, version=int(data.get("version", 1)))

    def find(self, milestone_id: str) -> Optional[Milestone]:
        for m in self.milestones:
            if m.id == milestone_id:
                return m
        return None


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_id(existing: Iterable[str], title: str) -> str:
    """Generate a stable, unique milestone ID based on the title."""
    base = re.sub(r"[^a-z0-9]+", "-", title.strip().lower()).strip("-")
    if not base:
        base = "milestone"
    candidate = base
    seen = set(existing)
    n = 1
    while candidate in seen:
        candidate = f"{base}-{n}"
        n += 1
    return candidate


def validate_date(value: Optional[str]) -> Optional[str]:
    """Validate an optional ISO date string. Returns None if undated."""
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise ValidationError("date must be a string or null")
    try:
        date.fromisoformat(value.strip())
    except ValueError as exc:
        raise ValidationError(f"invalid date '{value}' (use YYYY-MM-DD)") from exc
    return value.strip()


def validate_required_string(value: Any, field_name: str, max_len: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} is required")
    text = value.strip()
    if len(text) > max_len:
        raise ValidationError(f"{field_name} exceeds {max_len} characters")
    return text


def validate_optional_string(value: Any, field_name: str, max_len: int) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string")
    text = value.strip()
    if len(text) > max_len:
        raise ValidationError(f"{field_name} exceeds {max_len} characters")
    return text


def validate_entry_type(value: Any) -> str:
    text = validate_required_string(value, "entry_type", MAX_SOURCE_LEN)
    if text not in ENTRY_TYPES:
        raise ValidationError(
            f"entry_type must be one of {', '.join(ENTRY_TYPES)}"
        )
    return text


def validate_character(value: Any) -> str:
    return validate_required_string(value, "character", MAX_SOURCE_LEN)


def validate_category(value: Any) -> str:
    return validate_required_string(value, "category", MAX_CATEGORY_LEN)


def validate_source(value: Any) -> str:
    return validate_required_string(value, "source", MAX_SOURCE_LEN)


def validate_milestone(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and normalize a milestone dict. Raises ValidationError."""
    title = validate_required_string(data.get("title"), "title", MAX_TITLE_LEN)
    date_value = validate_date(data.get("date"))
    character = validate_character(data.get("character"))
    category = validate_category(data.get("category"))
    entry_type = validate_entry_type(data.get("entry_type"))
    description = validate_optional_string(
        data.get("description", ""), "description", MAX_DESCRIPTION_LEN
    )
    source = validate_source(data.get("source", "personal"))

    return {
        "title": title,
        "date": date_value,
        "character": character,
        "category": category,
        "entry_type": entry_type,
        "description": description,
        "source": source,
    }
