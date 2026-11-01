"""Tests for the Flask web application (routes, forms, validation)."""

import unittest

from lilyverse.storage import TimelineStorage
from lilyverse.web import create_app


class TestWeb(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmpdir = tempfile.mkdtemp()
        self.storage = TimelineStorage(data_dir=self.tmpdir)
        self.app = create_app(storage=self.storage)
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def _csrf_token(self, client):
        with client.session_transaction() as sess:
            return sess.get("csrf_token")

    def test_home_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"LilyVerse", response.data)
        self.assertIn(b"Eternal Bloom", response.data)

    def test_timeline_route(self):
        response = self.client.get("/timeline")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Interactive Timeline", response.data)

    def test_characters_route(self):
        response = self.client.get("/characters")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Character Archives", response.data)

    def test_character_detail_route(self):
        response = self.client.get("/characters/White Lily Cookie")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"White Lily Cookie", response.data)

    def test_character_detail_not_found(self):
        response = self.client.get("/characters/Not A Character")
        self.assertEqual(response.status_code, 404)

    def test_pla_route(self):
        response = self.client.get("/pla")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"PLA Memories", response.data)

    def test_memories_route(self):
        response = self.client.get("/memories")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Eternal Memory Garden", response.data)

    def _set_csrf_token(self, client, token="test-csrf-token"):
        with client.session_transaction() as sess:
            sess["csrf_token"] = token
        return token

    def test_add_milestone_get_and_post(self):
        response = self.client.get("/timeline/add")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add a Milestone", response.data)

        token = self._set_csrf_token(self.client)
        response = self.client.post("/timeline/add", data={
            "csrf_token": token,
            "title": "Web-added milestone",
            "date": "2026-10-29",
            "character": "Abinav",
            "category": "personal",
            "entry_type": "personal memory",
            "source": "personal",
            "description": "Added via web test.",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Web-added milestone", response.data)

    def test_add_milestone_validation_error(self):
        token = self._set_csrf_token(self.client)
        response = self.client.post("/timeline/add", data={
            "csrf_token": token,
            "title": "",  # invalid: required
            "date": "2026-10-29",
            "character": "Abinav",
            "category": "personal",
            "entry_type": "personal memory",
            "source": "personal",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"required", response.data.lower())

    def test_edit_milestone(self):
        m = self.storage.add_milestone({
            "title": "Editable", "date": "2026-10-24",
            "character": "Abinav", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        token = self._set_csrf_token(self.client)
        response = self.client.post(f"/timeline/edit/{m.id}", data={
            "csrf_token": token,
            "title": "Edited title",
            "date": "2026-10-25",
            "character": "Abinav",
            "category": "milestone",
            "entry_type": "personal memory",
            "source": "personal",
            "description": "Edited via web test.",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edited title", response.data)

    def test_delete_milestone(self):
        m = self.storage.add_milestone({
            "title": "Deletable", "date": "2026-10-24",
            "character": "Abinav", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        token = self._set_csrf_token(self.client)
        response = self.client.post(f"/timeline/delete/{m.id}", data={
            "csrf_token": token,
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_timeline_detail_not_found(self):
        response = self.client.get("/timeline/no-such-id")
        self.assertEqual(response.status_code, 404)

    def test_404_page(self):
        response = self.client.get("/no-such-page")
        self.assertEqual(response.status_code, 404)

    def test_csrf_protection(self):
        # POST without a valid CSRF token should be rejected (403)
        response = self.client.post("/timeline/add", data={
            "title": "No token",
            "date": "2026-10-29",
            "character": "Abinav",
            "category": "personal",
            "entry_type": "personal memory",
            "source": "personal",
        })
        self.assertEqual(response.status_code, 403)

    def test_search_and_filter(self):
        self.storage.add_milestone({
            "title": "Mogra Cookie memory", "date": "2026-10-24",
            "character": "Mogra Cookie", "category": "memory",
            "entry_type": "personal memory", "source": "personal",
        })
        response = self.client.get("/timeline?q=Mogra")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mogra Cookie memory", response.data)

    def test_stats_consistency(self):
        self.storage.add_milestone({
            "title": "Stat milestone", "date": "2026-10-24",
            "character": "White Lily Cookie", "category": "personal",
            "entry_type": "personal memory", "source": "personal",
        })
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Stat milestone", response.data)


if __name__ == "__main__":
    unittest.main()
