"""Tests for the shared JSON storage layer (models + storage)."""

import os
import tempfile
import unittest

from lilyverse.models import (
    ENTRY_TYPES,
    Milestone,
    ValidationError,
    validate_milestone,
)
from lilyverse.storage import StorageError, TimelineStorage


class TestModels(unittest.TestCase):
    def test_validate_milestone_minimal(self):
        data = validate_milestone({
            "title": "Test milestone",
            "date": "2026-10-29",
            "character": "Abinav",
            "category": "personal",
            "entry_type": "personal memory",
        })
        self.assertEqual(data["title"], "Test milestone")
        self.assertEqual(data["date"], "2026-10-29")
        self.assertEqual(data["entry_type"], "personal memory")

    def test_validate_milestone_undated(self):
        data = validate_milestone({
            "title": "Undated memory",
            "date": None,
            "character": "Abinav",
            "category": "personal",
            "entry_type": "personal memory",
        })
        self.assertIsNone(data["date"])

    def test_validate_milestone_missing_required(self):
        with self.assertRaises(ValidationError):
            validate_milestone({
                "title": "",
                "date": "2026-10-29",
                "character": "Abinav",
                "category": "personal",
                "entry_type": "personal memory",
            })

    def test_validate_milestone_bad_date(self):
        with self.assertRaises(ValidationError):
            validate_milestone({
                "title": "Bad date",
                "date": "not-a-date",
                "character": "Abinav",
                "category": "personal",
                "entry_type": "personal memory",
            })

    def test_validate_milestone_bad_entry_type(self):
        with self.assertRaises(ValidationError):
            validate_milestone({
                "title": "Bad type",
                "date": "2026-10-29",
                "character": "Abinav",
                "category": "personal",
                "entry_type": "not a real type",
            })

    def test_entry_types(self):
        self.assertIn("official fact", ENTRY_TYPES)
        self.assertIn("personal memory", ENTRY_TYPES)
        self.assertIn("fan interpretation", ENTRY_TYPES)


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.storage = TimelineStorage(data_dir=self.tmpdir)

    def test_init_creates_empty_data(self):
        data = self.storage.load()
        self.assertEqual(len(data.milestones), 0)

    def test_add_and_get_milestone(self):
        m = self.storage.add_milestone({
            "title": "White Lily tribute",
            "date": "2026-10-24",
            "character": "White Lily Cookie",
            "category": "personal",
            "entry_type": "personal memory",
            "description": "A tribute memory.",
            "source": "personal",
        })
        self.assertIsNotNone(m.id)
        fetched = self.storage.get_milestone(m.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.title, "White Lily tribute")
        self.assertEqual(fetched.character, "White Lily Cookie")

    def test_add_milestone_generates_stable_unique_id(self):
        m1 = self.storage.add_milestone({
            "title": "Lily memory", "date": "2026-10-24",
            "character": "White Lily Cookie", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        m2 = self.storage.add_milestone({
            "title": "Lily memory", "date": "2026-10-25",
            "character": "White Lily Cookie", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        self.assertNotEqual(m1.id, m2.id)

    def test_update_milestone(self):
        m = self.storage.add_milestone({
            "title": "Original", "date": "2026-10-24",
            "character": "Abinav", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        updated = self.storage.update_milestone(m.id, {
            "title": "Updated title",
            "date": "2026-10-25",
            "character": "Abinav",
            "category": "milestone",
            "entry_type": "fan interpretation",
            "description": "New description",
            "source": "fan",
        })
        self.assertEqual(updated.title, "Updated title")
        self.assertEqual(updated.date, "2026-10-25")
        self.assertEqual(updated.created_at, m.created_at)
        self.assertGreaterEqual(updated.updated_at, m.created_at)

    def test_update_nonexistent_raises(self):
        with self.assertRaises(StorageError):
            self.storage.update_milestone("does-not-exist", {
                "title": "x",
                "date": "2026-10-24",
                "character": "Abinav",
                "category": "personal",
                "entry_type": "personal memory",
                "source": "personal",
            })

    def test_delete_milestone(self):
        m = self.storage.add_milestone({
            "title": "To delete", "date": "2026-10-24",
            "character": "Abinav", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        removed = self.storage.delete_milestone(m.id)
        self.assertEqual(removed.id, m.id)
        self.assertIsNone(self.storage.get_milestone(m.id))

    def test_delete_nonexistent_raises(self):
        with self.assertRaises(StorageError):
            self.storage.delete_milestone("does-not-exist")

    def test_search(self):
        self.storage.add_milestone({
            "title": "White Lily tribute", "date": "2026-10-24",
            "character": "White Lily Cookie", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        self.storage.add_milestone({
            "title": "Pure Vanilla memory", "date": "2026-10-25",
            "character": "Pure Vanilla Cookie", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        results = self.storage.search("White Lily")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "White Lily tribute")

    def test_filter_by_character_and_category(self):
        self.storage.add_milestone({
            "title": "Mogra memory", "date": "2026-10-24",
            "character": "Mogra Cookie", "category": "memory",
            "entry_type": "personal memory", "source": "personal",
        })
        self.storage.add_milestone({
            "title": "Mogra milestone", "date": "2026-10-25",
            "character": "Mogra Cookie", "category": "milestone",
            "entry_type": "personal memory", "source": "personal",
        })
        chars = self.storage.filter_by(character="Mogra Cookie")
        self.assertEqual(len(chars), 2)
        cats = self.storage.filter_by(category="memory")
        self.assertEqual(len(cats), 1)
        self.assertEqual(cats[0].title, "Mogra memory")

    def test_sort_newest_and_oldest(self):
        self.storage.add_milestone({
            "title": "Older", "date": "2026-01-01",
            "character": "Abinav", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        self.storage.add_milestone({
            "title": "Newer", "date": "2026-12-31",
            "character": "Abinav", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        oldest = self.storage.sort_milestones(self.storage.list_milestones(), sort="oldest")
        newest = self.storage.sort_milestones(self.storage.list_milestones(), sort="newest")
        self.assertEqual(oldest[0].title, "Older")
        self.assertEqual(newest[0].title, "Newer")

    def test_undated_sorts_last(self):
        self.storage.add_milestone({
            "title": "Dated", "date": "2026-10-24",
            "character": "Abinav", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        self.storage.add_milestone({
            "title": "Undated", "date": None,
            "character": "Abinav", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        oldest = self.storage.sort_milestones(self.storage.list_milestones(), sort="oldest")
        self.assertEqual(oldest[-1].title, "Undated")

    def test_persistence_across_instances(self):
        m = self.storage.add_milestone({
            "title": "Persistent", "date": "2026-10-24",
            "character": "Abinav", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        storage2 = TimelineStorage(data_dir=self.tmpdir)
        fetched = storage2.get_milestone(m.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.title, "Persistent")

    def test_backup_and_restore(self):
        m = self.storage.add_milestone({
            "title": "Backup me", "date": "2026-10-24",
            "character": "Abinav", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        backup_path = self.storage.backup()
        self.assertTrue(os.path.exists(backup_path))

        self.storage.delete_milestone(m.id)
        self.assertIsNone(self.storage.get_milestone(m.id))

        safety = self.storage.restore(backup_path, confirm=True)
        self.assertTrue(os.path.exists(safety))
        restored = self.storage.get_milestone(m.id)
        self.assertIsNotNone(restored)
        self.assertEqual(restored.title, "Backup me")

    def test_restore_invalid_json_rejected(self):
        bad_path = os.path.join(self.tmpdir, "bad.json")
        with open(bad_path, "w") as f:
            f.write("{not valid json")
        with self.assertRaises(StorageError):
            self.storage.restore(bad_path, confirm=True)

    def test_restore_malformed_record_rejected(self):
        bad_path = os.path.join(self.tmpdir, "bad2.json")
        import json
        with open(bad_path, "w") as f:
            json.dump({"version": 1, "milestones": [{"title": ""}]}, f)
        with self.assertRaises((StorageError, ValidationError)):
            self.storage.restore(bad_path, confirm=True)

    def test_missing_data_file_initializes_empty(self):
        empty_dir = tempfile.mkdtemp()
        storage = TimelineStorage(data_dir=empty_dir)
        self.assertEqual(len(storage.list_milestones()), 0)

    def test_known_characters(self):
        chars = self.storage.known_characters()
        self.assertIn("White Lily Cookie", chars)
        self.assertIn("Pure Vanilla Cookie", chars)
        self.assertIn("Mogra Cookie", chars)
        self.assertIn("Abinav", chars)


if __name__ == "__main__":
    unittest.main()
