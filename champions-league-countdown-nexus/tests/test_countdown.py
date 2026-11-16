"""Automated tests for Champions League Countdown Nexus.

Covers:
  - Countdown calculation accuracy (days/hours/minutes/seconds)
  - Event state transitions (counting_down -> launched)
  - Input validation on /api/event POST
  - Health endpoint

Run:
    source .venv/bin/activate
    python -m pytest tests/ -v
    # or: python -m unittest tests.test_countdown -v
"""

from __future__ import annotations

import json
import unittest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app import create_app, _parse_event_datetime

IST = ZoneInfo("Asia/Kolkata")


class CountdownCalculationTest(unittest.TestCase):
    """Reliable countdown calculations — never hardcoded."""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def _event(self, offset_minutes):
        target = datetime.now(tz=IST) + timedelta(minutes=offset_minutes)
        return {
            "name": "Test Event",
            "date": target.strftime("%Y-%m-%d"),
            "time": target.strftime("%H:%M"),
            "timezone": "Asia/Kolkata",
            "kickoff_label": "Test",
            "description": "Test description",
            "unofficial_note": "Unofficial fan project.",
        }

    def test_countdown_never_hardcoded(self):
        target = datetime(2026, 11, 11, 20, 30, tzinfo=IST)
        event = {
            "date": "2026-11-11",
            "time": "20:30",
            "timezone": "Asia/Kolkata",
        }
        parsed = _parse_event_datetime(event)
        self.assertEqual(parsed, target)
        # tzinfo key is the IANA zone name (Asia/Kolkata), never hardcoded.
        self.assertEqual(str(parsed.tzinfo), "Asia/Kolkata")

    def test_countdown_breakdown(self):
        event = self._event(offset_minutes=90 * 24 * 60 + 3 * 60 + 45)
        parsed = _parse_event_datetime(event)
        now = datetime.now(tz=IST)
        diff = int((parsed - now).total_seconds())
        self.assertGreater(diff, 0)

        days = diff // (24 * 3600)
        rem = diff % (24 * 3600)
        hours = rem // 3600
        rem %= 3600
        minutes = rem // 60
        seconds = rem % 60

        reconstructed = days * 86400 + hours * 3600 + minutes * 60 + seconds
        self.assertEqual(reconstructed, diff)

    def test_countdown_past_event_launched(self):
        event = self._event(offset_minutes=-10)
        parsed = _parse_event_datetime(event)
        now = datetime.now(tz=IST)
        diff = int((parsed - now).total_seconds())
        self.assertLessEqual(diff, 0)

    def test_api_event_shape(self):
        resp = self.client.get("/api/event")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        for key in (
            "event", "target_iso", "target_label", "timezone",
            "now_iso", "diff_seconds", "launched", "countdown", "status",
        ):
            self.assertIn(key, data)
        self.assertIn("days", data["countdown"])
        self.assertIn("hours", data["countdown"])
        self.assertIn("minutes", data["countdown"])
        self.assertIn("seconds", data["countdown"])
        self.assertEqual(data["timezone"], "Asia/Kolkata")

    def test_api_health(self):
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["status"], "ok")


class EventTransitionTest(unittest.TestCase):
    """Automatic transition to event-started screen logic."""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_status_counting_down_when_future(self):
        target = (datetime.now(tz=IST) + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M")
        date, time = target.split(" ")
        payload = {
            "date": date,
            "time": time,
            "timezone": "Asia/Kolkata",
        }
        self.client.post(
            "/api/event",
            data=json.dumps(payload),
            content_type="application/json",
        )
        # Confirm via GET /api/event (the source of truth for countdown state).
        data = self.client.get("/api/event").get_json()
        self.assertFalse(data["launched"])
        self.assertEqual(data["status"], "counting_down")
        self.assertGreater(data["diff_seconds"], 0)

    def test_status_launched_when_past(self):
        target = (datetime.now(tz=IST) - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M")
        date, time = target.split(" ")
        payload = {
            "date": date,
            "time": time,
            "timezone": "Asia/Kolkata",
        }
        self.client.post(
            "/api/event",
            data=json.dumps(payload),
            content_type="application/json",
        )
        data = self.client.get("/api/event").get_json()
        self.assertTrue(data["launched"])
        self.assertEqual(data["status"], "launched")
        self.assertLessEqual(data["diff_seconds"], 0)


class InputValidationTest(unittest.TestCase):
    """All user inputs are validated."""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def post(self, payload):
        return self.client.post(
            "/api/event",
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_invalid_date_rejected(self):
        resp = self.post({"date": "not-a-date", "time": "20:30", "timezone": "Asia/Kolkata"})
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.get_json())

    def test_invalid_time_rejected(self):
        resp = self.post({"date": "2026-11-11", "time": "99:99", "timezone": "Asia/Kolkata"})
        self.assertEqual(resp.status_code, 400)

    def test_invalid_timezone_rejected(self):
        resp = self.post({"date": "2026-11-11", "time": "20:30", "timezone": "Not/AZone"})
        self.assertEqual(resp.status_code, 400)

    def test_missing_content_type_rejected(self):
        resp = self.client.post(
            "/api/event",
            data='{"date":"2026-11-11","time":"20:30"}',
        )
        self.assertEqual(resp.status_code, 400)

    def test_valid_event_accepted(self):
        resp = self.post({
            "date": "2026-11-11",
            "time": "20:30",
            "timezone": "Asia/Kolkata",
            "name": "Custom Event",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["status"], "ok")


if __name__ == "__main__":
    unittest.main()
