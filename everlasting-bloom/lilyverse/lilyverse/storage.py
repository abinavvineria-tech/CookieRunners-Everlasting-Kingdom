"""Persistent JSON storage for LilyVerse.

Provides a single shared JSON data store used by both the CLI and the Flask
website. Writes are atomic (temp file + os.replace) and protected by a simple
file lock so concurrent writers don't corrupt each other.
"""

from __future__ import annotations

import fcntl
import json
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from lilyverse.models import (
    CHARACTERS,
    DEFAULT_CATEGORIES,
    DEFAULT_SOURCES,
    Milestone,
    TimelineData,
    generate_id,
    now_iso,
    validate_milestone,
)

DATA_DIR_NAME = "data"
BACKUPS_DIR_NAME = "backups"
DEFAULT_DATA_FILENAME = "timeline.json"


class StorageError(Exception):
    """Raised when the data store cannot be read or written."""


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


@contextmanager
def _file_lock(lock_path: str):
    """Simple exclusive file lock using fcntl (Unix/Termux/Ubuntu)."""
    _ensure_dir(os.path.dirname(lock_path))
    lock_fd = open(lock_path, "w")
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        yield
    finally:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        finally:
            lock_fd.close()


class TimelineStorage:
    """Reads/writes the shared JSON timeline store."""

    def __init__(self, data_dir: Optional[str] = None, data_filename: str = DEFAULT_DATA_FILENAME):
        if data_dir is None:
            # Default: <package_root>/data
            here = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(here, DATA_DIR_NAME)
        self.data_dir = os.path.abspath(data_dir)
        self.data_path = os.path.join(self.data_dir, data_filename)
        self.backups_dir = os.path.join(os.path.dirname(self.data_dir), BACKUPS_DIR_NAME)
        self.lock_path = os.path.join(self.data_dir, ".timeline.lock")
        _ensure_dir(self.data_dir)
        _ensure_dir(self.backups_dir)

    # ------------------------------------------------------------------ #
    # Low-level read / write
    # ------------------------------------------------------------------ #
    def _read_locked(self) -> TimelineData:
        if not os.path.exists(self.data_path):
            return TimelineData()
        with _file_lock(self.lock_path):
            return self._read_unlocked()

    def _read_unlocked(self) -> TimelineData:
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                raw = f.read()
        except FileNotFoundError:
            return TimelineData()
        if not raw.strip():
            return TimelineData()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise StorageError(f"corrupt JSON in {self.data_path}: {exc}") from exc
        if not isinstance(data, dict):
            raise StorageError("timeline data root must be a JSON object")
        return TimelineData.from_dict(data)

    def _write_locked(self, data: TimelineData) -> None:
        with _file_lock(self.lock_path):
            self._write_unlocked(data)

    def _write_unlocked(self, data: TimelineData) -> None:
        payload = json.dumps(data.to_dict(), indent=2, ensure_ascii=False) + "\n"
        # Atomic write: temp file in same dir, then os.replace.
        dir_fd = os.open(self.data_dir, os.O_RDONLY)
        try:
            fd, tmp_path = tempfile.mkstemp(
                prefix=".timeline-", suffix=".tmp", dir=self.data_dir
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(payload)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp_path, self.data_path)
            except BaseException:
                try:
                    os.unlink(tmp_path)
                except FileNotFoundError:
                    pass
                raise
        finally:
            try:
                os.close(dir_fd)
            except OSError:
                pass

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def load(self) -> TimelineData:
        return self._read_locked()

    def save(self, data: TimelineData) -> None:
        self._write_locked(data)

    def list_milestones(self) -> List[Milestone]:
        return list(self._read_locked().milestones)

    def get_milestone(self, milestone_id: str) -> Optional[Milestone]:
        return self._read_locked().find(milestone_id)

    def add_milestone(self, raw: Dict[str, Any]) -> Milestone:
        """Validate, assign timestamps/ID, and append a milestone."""
        cleaned = validate_milestone(raw)
        data = self._read_locked()
        existing_ids = [m.id for m in data.milestones]
        milestone_id = generate_id(existing_ids, cleaned["title"])
        now = now_iso()
        milestone = Milestone(
            id=milestone_id,
            title=cleaned["title"],
            date=cleaned["date"],
            character=cleaned["character"],
            category=cleaned["category"],
            entry_type=cleaned["entry_type"],
            description=cleaned["description"],
            source=cleaned["source"],
            created_at=now,
            updated_at=now,
        )
        data.milestones.append(milestone)
        self._write_unlocked(data)
        return milestone

    def update_milestone(self, milestone_id: str, raw: Dict[str, Any]) -> Milestone:
        """Validate and replace an existing milestone (keeps id/created_at)."""
        cleaned = validate_milestone(raw)
        data = self._read_locked()
        for idx, m in enumerate(data.milestones):
            if m.id == milestone_id:
                updated = Milestone(
                    id=milestone_id,
                    title=cleaned["title"],
                    date=cleaned["date"],
                    character=cleaned["character"],
                    category=cleaned["category"],
                    entry_type=cleaned["entry_type"],
                    description=cleaned["description"],
                    source=cleaned["source"],
                    created_at=m.created_at,
                    updated_at=now_iso(),
                )
                data.milestones[idx] = updated
                self._write_unlocked(data)
                return updated
        raise StorageError(f"milestone {milestone_id!r} not found")

    def delete_milestone(self, milestone_id: str) -> Milestone:
        """Remove a milestone and return it. Raises if not found."""
        data = self._read_locked()
        for idx, m in enumerate(data.milestones):
            if m.id == milestone_id:
                removed = data.milestones.pop(idx)
                self._write_unlocked(data)
                return removed
        raise StorageError(f"milestone {milestone_id!r} not found")

    def search(self, query: str) -> List[Milestone]:
        q = query.lower()
        return [
            m
            for m in self._read_locked().milestones
            if q in m.title.lower() or q in m.description.lower() or q in m.character.lower()
        ]

    def filter_by(self, character: Optional[str] = None, category: Optional[str] = None) -> List[Milestone]:
        milestones = self._read_locked().milestones
        if character:
            milestones = [m for m in milestones if m.character == character]
        if category:
            milestones = [m for m in milestones if m.category == category]
        return milestones

    def sort_milestones(self, milestones: List[Milestone], sort: str = "oldest") -> List[Milestone]:
        def sort_key(m: Milestone):
            # Undated items sort last; within, use ISO date string.
            return (m.date is None, m.date or "")

        reverse = sort == "newest"
        return sorted(milestones, key=sort_key, reverse=reverse)

    # ------------------------------------------------------------------ #
    # Backup / restore
    # ------------------------------------------------------------------ #
    def backup(self, backup_path: Optional[str] = None) -> str:
        """Write a timestamped backup of the current data file."""
        _ensure_dir(self.backups_dir)
        if backup_path is None:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup_path = os.path.join(self.backups_dir, f"timeline-{stamp}.json")
        backup_path = os.path.abspath(backup_path)
        # Safety: never write outside the project data/backups trees.
        allowed_roots = [os.path.abspath(self.data_dir), os.path.abspath(self.backups_dir)]
        if not any(
            backup_path == root or backup_path.startswith(root + os.sep)
            for root in allowed_roots
        ):
            raise StorageError(
                f"backup path {backup_path} is outside allowed project directories"
            )
        data = self._read_locked()
        payload = json.dumps(data.to_dict(), indent=2, ensure_ascii=False) + "\n"
        _ensure_dir(os.path.dirname(backup_path))
        dir_fd = os.open(os.path.dirname(backup_path), os.O_RDONLY)
        try:
            fd, tmp_path = tempfile.mkstemp(prefix=".backup-", suffix=".tmp", dir=os.path.dirname(backup_path))
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(payload)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp_path, backup_path)
            except BaseException:
                try:
                    os.unlink(tmp_path)
                except FileNotFoundError:
                    pass
                raise
        finally:
            try:
                os.close(dir_fd)
            except OSError:
                pass
        return backup_path

    def restore(self, backup_path: str, confirm: bool = False) -> str:
        """Restore data from a backup file.

        Validates structure first, keeps a safety backup of current data,
        and never overwrites arbitrary files outside the data directory.
        """
        backup_path = os.path.abspath(backup_path)
        if not os.path.exists(backup_path):
            raise StorageError(f"backup file not found: {backup_path}")

        # Load and validate the backup structure without touching live data.
        with open(backup_path, "r", encoding="utf-8") as f:
            raw = f.read()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise StorageError(f"invalid JSON in backup: {exc}") from exc
        if not isinstance(data, dict) or "milestones" not in data:
            raise StorageError("backup does not contain a valid timeline structure")
        # Validate every milestone record.
        for m in data.get("milestones", []):
            validate_milestone(m)  # will raise ValidationError on bad records

        # Safety backup before replacing live data.
        safety = self.backup()

        # Only restore into the intended data file.
        self._write_unlocked(TimelineData.from_dict(data))
        return safety

    # ------------------------------------------------------------------ #
    # Character registry (user-extensible without editing source)
    # ------------------------------------------------------------------ #
    def known_characters(self) -> Dict[str, Dict[str, str]]:
        return dict(CHARACTERS)

    def is_known_character(self, name: str) -> bool:
        return name in CHARACTERS
