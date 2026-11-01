"""Tests for the LilyVerse CLI."""

import io
import re
import tempfile
import unittest

from lilyverse.cli import build_parser
from lilyverse.services import LilyVerseService
from lilyverse.storage import TimelineStorage


class _CaptureOut:
    """Minimal output object capturing to a string buffer (plain-text, no Rich)."""

    def __init__(self):
        self.buf = io.StringIO()
        self.use_rich = False

    def print(self, *a, **k):
        print(*a, file=self.buf, **k)

    def header(self, text, style=None):
        self.buf.write(f"== {text} ==\n")

    def table(self, title, columns, rows, style=None):
        self.buf.write(f"{title}\n")
        self.buf.write(" | ".join(columns) + "\n")
        for r in rows:
            self.buf.write(" | ".join(r) + "\n")

    def kv(self, title, pairs):
        self.buf.write(f"{title}\n")
        for k, v in pairs:
            self.buf.write(f"  {k}: {v}\n")

    def success(self, text):
        self.buf.write(f"✓ {text}\n")

    def error(self, text):
        self.buf.write(f"✗ {text}\n")

    def info(self, text):
        self.buf.write(f"{text}\n")


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.storage = TimelineStorage(data_dir=self.tmpdir)

    def _run(self, argv):
        parser = build_parser()
        args = parser.parse_args(argv)
        out = _CaptureOut()
        service = LilyVerseService(self.storage)
        try:
            code = args.func(args, out, service)
        except SystemExit as e:
            code = e.code if e.code is not None else 0
        return code, out.buf.getvalue()

    def test_help(self):
        parser = build_parser()
        with self.assertRaises(SystemExit) as cm:
            parser.parse_args(["--help"])
        self.assertEqual(cm.exception.code, 0)

    def test_version(self):
        code, output = self._run(["version"])
        self.assertEqual(code, 0)
        self.assertIn("1.0.0", output)
        self.assertIn("Eternal Bloom", output)

    def test_dashboard(self):
        code, output = self._run(["dashboard"])
        self.assertEqual(code, 0)
        self.assertIn("Dashboard", output)
        self.assertIn("Total milestones", output)

    def test_timeline_list_empty(self):
        code, output = self._run(["timeline", "list"])
        self.assertEqual(code, 0)

    def test_timeline_add_and_list(self):
        code, output = self._run(["timeline", "add",
            "--title", "CLI milestone",
            "--date", "2026-10-29",
            "--character", "Abinav",
            "--category", "personal",
            "--entry-type", "personal memory",
            "--source", "personal",
            "--description", "Added via CLI test",
        ])
        self.assertEqual(code, 0)
        self.assertIn("CLI milestone", output)

        code, output = self._run(["timeline", "list"])
        self.assertEqual(code, 0)
        self.assertIn("CLI milestone", output)

    def test_timeline_list_filters(self):
        self._run(["timeline", "add",
            "--title", "Filter me", "--date", "2026-10-29",
            "--character", "White Lily Cookie",
            "--category", "personal",
            "--entry-type", "personal memory",
            "--source", "personal",
        ])
        code, output = self._run(["timeline", "list", "--character", "White Lily Cookie"])
        self.assertEqual(code, 0)
        self.assertIn("Filter me", output)

        code, output = self._run(["timeline", "list", "--sort", "newest"])
        self.assertEqual(code, 0)

        code, output = self._run(["timeline", "list", "--search", "Filter"])
        self.assertEqual(code, 0)
        self.assertIn("Filter me", output)

    def test_timeline_show(self):
        code, output = self._run(["timeline", "add",
            "--title", "Show me", "--date", "2026-10-29",
            "--character", "Abinav", "--category", "personal",
            "--entry-type", "personal memory", "--source", "personal",
        ])
        match = re.search(r"Added milestone (\S+):", output)
        self.assertIsNotNone(match)
        mid = match.group(1)

        code, output = self._run(["timeline", "show", mid])
        self.assertEqual(code, 0)
        self.assertIn("Show me", output)

    def test_timeline_show_not_found(self):
        code, output = self._run(["timeline", "show", "no-such-id"])
        self.assertEqual(code, 1)

    def test_timeline_search(self):
        self._run(["timeline", "add",
            "--title", "White Lily tribute",
            "--date", "2026-10-24", "--character", "White Lily Cookie",
            "--category", "personal", "--entry-type", "personal memory",
            "--source", "personal",
        ])
        code, output = self._run(["timeline", "search", "White Lily"])
        self.assertEqual(code, 0)
        self.assertIn("White Lily tribute", output)

    def test_timeline_edit(self):
        code, output = self._run(["timeline", "add",
            "--title", "Before edit", "--date", "2026-10-24",
            "--character", "Abinav", "--category", "personal",
            "--entry-type", "personal memory", "--source", "personal",
        ])
        match = re.search(r"Added milestone (\S+):", output)
        mid = match.group(1)

        code, output = self._run(["timeline", "edit", mid, "--title", "After edit"])
        self.assertEqual(code, 0)
        self.assertIn("Updated milestone", output)

    def test_timeline_delete_confirmed(self):
        code, output = self._run(["timeline", "add",
            "--title", "To delete", "--date", "2026-10-24",
            "--character", "Abinav", "--category", "personal",
            "--entry-type", "personal memory", "--source", "personal",
        ])
        match = re.search(r"Added milestone (\S+):", output)
        mid = match.group(1)

        code, output = self._run(["timeline", "delete", mid, "--yes"])
        self.assertEqual(code, 0)

        code, output = self._run(["timeline", "show", mid])
        self.assertEqual(code, 1)

    def test_characters_list(self):
        code, output = self._run(["characters", "list"])
        self.assertEqual(code, 0)
        self.assertIn("White Lily Cookie", output)

    def test_characters_show(self):
        code, output = self._run(["characters", "show", "Mogra Cookie"])
        self.assertEqual(code, 0)
        self.assertIn("Mogra Cookie", output)

    def test_characters_show_not_found(self):
        code, output = self._run(["characters", "show", "Not A Character"])
        self.assertEqual(code, 1)

    def test_memories_list(self):
        code, output = self._run(["memories", "list"])
        self.assertEqual(code, 0)
        self.assertIn("PLA Memories", output)

    def test_stats(self):
        code, output = self._run(["stats"])
        self.assertEqual(code, 0)
        self.assertIn("Statistics", output)

    def test_backup(self):
        code, output = self._run(["backup"])
        self.assertEqual(code, 0)

    def test_add_missing_required_rejected(self):
        code, output = self._run(["timeline", "add"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
