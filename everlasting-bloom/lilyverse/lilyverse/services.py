"""Shared services used by both the CLI and the Flask website.

Keeps business logic in one place so the two interfaces always reflect the
same data.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from lilyverse.models import Milestone, TimelineData
from lilyverse.storage import TimelineStorage


class LilyVerseService:
    def __init__(self, storage: TimelineStorage):
        self.storage = storage

    # -- milestones ---------------------------------------------------- #
    def list_milestones(
        self,
        character: Optional[str] = None,
        category: Optional[str] = None,
        sort: str = "oldest",
        query: Optional[str] = None,
    ) -> List[Milestone]:
        milestones = self.storage.filter_by(character=character, category=category)
        if query:
            milestones = self.storage.search(query)
            # Re-apply character/category filters on top of search.
            if character:
                milestones = [m for m in milestones if m.character == character]
            if category:
                milestones = [m for m in milestones if m.category == category]
        return self.storage.sort_milestones(milestones, sort=sort)

    def get_milestone(self, milestone_id: str) -> Optional[Milestone]:
        return self.storage.get_milestone(milestone_id)

    def add_milestone(self, raw: Dict[str, Any]) -> Milestone:
        return self.storage.add_milestone(raw)

    def update_milestone(self, milestone_id: str, raw: Dict[str, Any]) -> Milestone:
        return self.storage.update_milestone(milestone_id, raw)

    def delete_milestone(self, milestone_id: str) -> Milestone:
        return self.storage.delete_milestone(milestone_id)

    def search_milestones(self, query: str) -> List[Milestone]:
        return self.storage.search(query)

    # -- stats --------------------------------------------------------- #
    def stats(self) -> Dict[str, Any]:
        milestones = self.storage.list_milestones()
        by_character: Dict[str, int] = {}
        by_category: Dict[str, int] = {}
        by_year: Dict[str, int] = {}
        dates: List[str] = []
        for m in milestones:
            by_character[m.character] = by_character.get(m.character, 0) + 1
            by_category[m.category] = by_category.get(m.category, 0) + 1
            if m.date:
                year = m.date[:4]
                by_year[year] = by_year.get(year, 0) + 1
                dates.append(m.date)
        dates.sort()
        return {
            "total": len(milestones),
            "by_character": by_character,
            "by_category": by_category,
            "by_year": by_year,
            "earliest": dates[0] if dates else None,
            "latest": dates[-1] if dates else None,
        }

    # -- characters ---------------------------------------------------- #
    def known_characters(self) -> Dict[str, Dict[str, str]]:
        return self.storage.known_characters()

    # -- backup / restore ---------------------------------------------- #
    def backup(self, backup_path: Optional[str] = None) -> str:
        return self.storage.backup(backup_path)

    def restore(self, backup_path: str, confirm: bool = False) -> str:
        return self.storage.restore(backup_path, confirm=confirm)
