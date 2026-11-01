"""LilyVerse command-line interface.

Powered by argparse. Optional Rich styling when installed, with a clean
plain-text fallback when Rich is unavailable. All commands operate on the same
shared JSON data store used by the Flask website.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from lilyverse.models import (
    ENTRY_TYPES,
    Milestone,
    ValidationError,
    now_iso,
    validate_milestone,
)
from lilyverse.services import LilyVerseService
from lilyverse.storage import StorageError, TimelineStorage


# --------------------------------------------------------------------------- #
# Optional Rich output
# --------------------------------------------------------------------------- #
try:  # Rich is optional
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    _HAS_RICH = True
except Exception:  # pragma: no cover - Rich not installed
    _HAS_RICH = False


class _Output:
    """Unified output: Rich when available, plain text otherwise."""

    def __init__(self, use_rich: bool = True):
        self.use_rich = use_rich and _HAS_RICH
        if self.use_rich:
            self.console = Console()

    def print(self, *args, **kwargs):
        if self.use_rich:
            self.console.print(*args, **kwargs)
        else:
            print(*args, **kwargs)

    def header(self, text: str, style: str = "bold magenta"):
        if self.use_rich:
            self.console.print(Panel(text, style=style, expand=False))
        else:
            print(f"== {text} ==")

    def table(
        self,
        title: str,
        columns: List[str],
        rows: List[List[str]],
        style: str = "bold cyan",
    ):
        if self.use_rich:
            t = Table(title=title, header_style=style)
            for c in columns:
                t.add_column(c)
            for r in rows:
                t.add_row(*r)
            self.console.print(t)
        else:
            print(f"\n{title}")
            print(" | ".join(columns))
            print("-" * (sum(len(c) for c in columns) + 3 * (len(columns) - 1)))
            for r in rows:
                print(" | ".join(r))

    def kv(self, title: str, pairs: List[tuple]):
        if self.use_rich:
            self.console.print(f"\n[bold]{title}[/bold]")
            for k, v in pairs:
                self.console.print(f"  [cyan]{k}:[/cyan] {v}")
        else:
            print(f"\n{title}")
            for k, v in pairs:
                print(f"  {k}: {v}")

    def success(self, text: str):
        if self.use_rich:
            self.console.print(f"[bold green]✓[/bold green] {text}")
        else:
            print(f"✓ {text}")

    def error(self, text: str):
        if self.use_rich:
            self.console.print(f"[bold red]✗[/bold red] {text}")
        else:
            print(f"✗ {text}")

    def info(self, text: str):
        if self.use_rich:
            self.console.print(f"[dim]{text}[/dim]")
        else:
            print(text)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _prompt(prompt: str, default: Optional[str] = None) -> str:
    if default is not None:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    value = input(prompt).strip()
    if not value and default is not None:
        return default
    return value


def _confirm(prompt: str) -> bool:
    answer = input(f"{prompt} [y/N]: ").strip().lower()
    return answer in ("y", "yes")


def _parse_args(raw: List[str]) -> Dict[str, str]:
    """Parse ``key=value`` style extra args into a dict."""
    result: Dict[str, str] = {}
    for item in raw:
        if "=" in item:
            k, v = item.split("=", 1)
            result[k.strip()] = v.strip()
    return result


def _format_milestone(out: _Output, m: Milestone) -> None:
    pairs = [
        ("ID", m.id),
        ("Title", m.title),
        ("Date", m.date or "(undated)"),
        ("Character", m.character),
        ("Category", m.category),
        ("Entry type", m.entry_type),
        ("Source", m.source),
        ("Description", m.description or "(none)"),
        ("Created", m.created_at),
        ("Updated", m.updated_at),
    ]
    out.kv(f"Milestone — {m.title}", pairs)


# --------------------------------------------------------------------------- #
# Command implementations
# --------------------------------------------------------------------------- #
def cmd_version(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    from lilyverse import __version__, __tagline__
    out.header("LilyVerse — The Eternal Bloom Timeline")
    out.kv("Details", [
        ("Version", __version__),
        ("Tagline", __tagline__),
        ("Unofficial fan project", "Yes — not affiliated with Devsisters"),
    ])
    return 0


def cmd_dashboard(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    stats = service.stats()
    storage = service.storage

    out.header("LilyVerse Dashboard")
    out.kv("Overview", [
        ("Version", "1.0.0"),
        ("Total milestones", str(stats["total"])),
        ("Data file", storage.data_path),
        ("Unofficial fan project", "Yes — not affiliated with Devsisters"),
    ])

    if stats["by_character"]:
        rows = [[ch, str(cnt)] for ch, cnt in sorted(stats["by_character"].items())]
        out.table("Milestones by Character", ["Character", "Count"], rows)

    if stats["by_year"]:
        rows = [[yr, str(cnt)] for yr, cnt in sorted(stats["by_year"].items())]
        out.table("Milestones by Year", ["Year", "Count"], rows)

    if stats["earliest"]:
        out.kv("Timeline range", [
            ("Earliest", stats["earliest"]),
            ("Latest", stats["latest"]),
        ])

    # Most recent milestone
    milestones = service.list_milestones(sort="newest")
    if milestones:
        m = milestones[0]
        out.kv("Most recent milestone", [
            ("Title", m.title),
            ("Date", m.date or "(undated)"),
            ("Character", m.character),
        ])

    # Website status (local check only)
    out.info("Website: run `python app.py` or `python -m lilyverse web`, then open http://127.0.0.1:5000")
    return 0


def cmd_timeline_list(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    milestones = service.list_milestones(
        character=args.character,
        category=args.category,
        sort=args.sort,
        query=args.search,
    )
    if not milestones:
        out.info("No milestones found.")
        return 0

    columns = ["ID", "Date", "Character", "Category", "Title"]
    rows = [
        [m.id, m.date or "—", m.character, m.category, m.title]
        for m in milestones
    ]
    out.table("Timeline Milestones", columns, rows)
    out.info(f"{len(milestones)} milestone(s). Use `timeline show <ID>` for details.")
    return 0


def cmd_timeline_show(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    m = service.get_milestone(args.id)
    if m is None:
        out.error(f"Milestone {args.id!r} not found.")
        return 1
    _format_milestone(out, m)
    return 0


def _prompt_milestone(existing: Optional[Milestone] = None, out: _Output = None) -> Dict[str, Any]:
    out = out or _Output(use_rich=False)
    title = _prompt("Title", existing.title if existing else "")
    date = _prompt("Date (YYYY-MM-DD, or leave blank for undated)", existing.date if existing else "")
    character = _prompt("Character", existing.character if existing else "Abinav")
    category = _prompt("Category", existing.category if existing else "personal")
    print("Entry types: official fact, personal memory, fan interpretation")
    entry_type = _prompt("Entry type", existing.entry_type if existing else "personal memory")
    description = _prompt("Description", existing.description if existing else "")
    source = _prompt("Source (official/personal/fan)", existing.source if existing else "personal")
    return {
        "title": title,
        "date": date or None,
        "character": character,
        "category": category,
        "entry_type": entry_type,
        "description": description,
        "source": source,
    }


def cmd_timeline_add(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    raw: Dict[str, Any] = {
        "title": args.title,
        "date": args.date or None,
        "character": args.character,
        "category": args.category,
        "entry_type": args.entry_type,
        "description": args.description,
        "source": args.source,
    }
    missing = []
    if not raw["title"]:
        missing.append("title")
    if not raw["character"]:
        missing.append("character")
    if not raw["category"]:
        missing.append("category")
    if not raw["entry_type"]:
        missing.append("entry_type")

    if missing and not args.interactive:
        out.error("Missing required fields: " + ", ".join(missing))
        out.info("Run without flags to be prompted interactively, or pass --title --character etc.")
        return 1

    if missing or args.interactive:
        prompted = _prompt_milestone(
            existing=None, out=out
        )
        # Merge: prompted values fill in the blanks; explicit flags take precedence when non-empty.
        for key in ("title", "date", "character", "category", "entry_type", "description", "source"):
            if raw.get(key):
                prompted[key] = raw[key]
        # normalize date: prompted may be empty string
        if prompted.get("date") == "":
            prompted["date"] = None
        raw = prompted

    try:
        m = service.add_milestone(raw)
    except ValidationError as exc:
        out.error(f"Validation failed: {exc}")
        return 1
    except StorageError as exc:
        out.error(f"Storage error: {exc}")
        return 1

    out.success(f"Added milestone {m.id}: {m.title}")
    return 0


def cmd_timeline_search(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    milestones = service.search_milestones(args.query)
    if not milestones:
        out.info(f"No milestones match '{args.query}'.")
        return 0
    columns = ["ID", "Date", "Character", "Category", "Title"]
    rows = [[m.id, m.date or "—", m.character, m.category, m.title] for m in milestones]
    out.table(f"Search results for '{args.query}'", columns, rows)
    return 0


def cmd_timeline_edit(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    m = service.get_milestone(args.id)
    if m is None:
        out.error(f"Milestone {args.id!r} not found.")
        return 1

    raw: Dict[str, Any] = {
        "title": args.title,
        "date": args.date or None,
        "character": args.character,
        "category": args.category,
        "entry_type": args.entry_type,
        "description": args.description,
        "source": args.source,
    }

    if args.interactive or all(not v for v in raw.values()):
        out.info(f"Editing {m.id} — {m.title} (leave blank to keep current value)")
        prompted = _prompt_milestone(existing=m, out=out)
        for key in ("title", "date", "character", "category", "entry_type", "description", "source"):
            if raw.get(key):
                prompted[key] = raw[key]
        # keep existing value if prompted returned empty for a non-required optional
        for key in ("title", "character", "category", "entry_type", "source"):
            if not prompted.get(key):
                prompted[key] = getattr(m, key)
        if prompted.get("date") == "":
            prompted["date"] = m.date
        raw = prompted

    # Always preserve at least the existing values for anything not provided.
    final: Dict[str, Any] = {
        "title": raw.get("title") or m.title,
        "date": raw.get("date") if raw.get("date") is not None else m.date,
        "character": raw.get("character") or m.character,
        "category": raw.get("category") or m.category,
        "entry_type": raw.get("entry_type") or m.entry_type,
        "description": raw.get("description") if raw.get("description") is not None else m.description,
        "source": raw.get("source") or m.source,
    }

    try:
        updated = service.update_milestone(args.id, final)
    except ValidationError as exc:
        out.error(f"Validation failed: {exc}")
        return 1
    except StorageError as exc:
        out.error(f"Storage error: {exc}")
        return 1

    out.success(f"Updated milestone {updated.id}: {updated.title}")
    return 0


def cmd_timeline_delete(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    m = service.get_milestone(args.id)
    if m is None:
        out.error(f"Milestone {args.id!r} not found.")
        return 1

    if not args.yes:
        out.info(f"About to delete: {m.id} — {m.title}")
        if not _confirm("Delete this milestone?"):
            out.info("Delete cancelled.")
            return 0

    try:
        removed = service.delete_milestone(args.id)
    except StorageError as exc:
        out.error(str(exc))
        return 1

    out.success(f"Deleted milestone {removed.id}: {removed.title}")
    return 0


# -- characters --------------------------------------------------------- #
def cmd_characters_list(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    chars = service.known_characters()
    if not chars:
        out.info("No character profiles defined.")
        return 0
    columns = ["Character", "Role", "Origin"]
    rows = [[name, info.get("role", ""), info.get("origin", "")] for name, info in chars.items()]
    out.table("Character Archives", columns, rows)
    return 0


def cmd_characters_show(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    chars = service.known_characters()
    if args.name not in chars:
        out.error(f"Character {args.name!r} not found.")
        out.info("Known: " + ", ".join(sorted(chars)))
        return 1
    info = chars[args.name]
    out.kv(f"Character — {args.name}", [
        ("Role", info.get("role", "")),
        ("Description", info.get("description", "")),
        ("Origin", info.get("origin", "")),
    ])
    # Associated milestones
    assoc = [m for m in service.list_milestones() if m.character == args.name]
    if assoc:
        rows = [[m.id, m.date or "—", m.category, m.title] for m in assoc]
        out.table(f"Milestones for {args.name}", ["ID", "Date", "Category", "Title"], rows)
    else:
        out.info(f"No milestones associated with {args.name} yet.")
    return 0


# -- memories (PLA) ----------------------------------------------------- #
def cmd_memories_list(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    # PLA trio: Pure Vanilla Cookie, White Lily Cookie, Abinav
    trio = ["Pure Vanilla Cookie", "White Lily Cookie", "Abinav"]
    out.header("PLA Memories — Pure Vanilla, White Lily & Abinav")
    for name in trio:
        assoc = [m for m in service.list_milestones() if m.character == name]
        out.kv(name, [
            ("Associated milestones", str(len(assoc))),
            ("Latest", assoc[0].title if assoc else "(none)"),
        ])
    return 0


# -- stats -------------------------------------------------------------- #
def cmd_stats(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    stats = service.stats()
    out.header("LilyVerse Statistics")
    out.kv("Totals", [
        ("Total milestones", str(stats["total"])),
        ("Earliest", stats["earliest"] or "(none)"),
        ("Latest", stats["latest"] or "(none)"),
    ])
    if stats["by_character"]:
        rows = [[ch, str(cnt)] for ch, cnt in sorted(stats["by_character"].items())]
        out.table("By Character", ["Character", "Count"], rows)
    if stats["by_category"]:
        rows = [[cat, str(cnt)] for cat, cnt in sorted(stats["by_category"].items())]
        out.table("By Category", ["Category", "Count"], rows)
    if stats["by_year"]:
        rows = [[yr, str(cnt)] for yr, cnt in sorted(stats["by_year"].items())]
        out.table("By Year", ["Year", "Count"], rows)
    return 0


# -- web ---------------------------------------------------------------- #
def cmd_web(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    import os
    import subprocess

    host = os.environ.get("LILYVERSE_HOST", "127.0.0.1")
    port = os.environ.get("LILYVERSE_PORT", "5000")
    out.info(f"Starting Flask website on http://{host}:{port}")
    out.info("Debug mode is disabled by default. Set LILYVERSE_DEBUG=1 for development.")
    out.info("Press Ctrl+C to stop.")
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        out.info("Website stopped.")
        return 0
    except FileNotFoundError:
        out.error("app.py not found in the current directory.")
        out.info("Run `python -m lilyverse web` from the lilyverse project root.")
        return 1
    return 0


# -- backup / restore --------------------------------------------------- #
def cmd_backup(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    try:
        path = service.backup(args.file)
    except StorageError as exc:
        out.error(str(exc))
        return 1
    out.success(f"Backup written to {path}")
    return 0


def cmd_restore(args: argparse.Namespace, out: _Output, service: LilyVerseService) -> int:
    if not args.yes:
        out.info(f"About to restore from {args.file}")
        out.info("A safety backup of current data will be created first.")
        if not _confirm("Proceed with restore?"):
            out.info("Restore cancelled.")
            return 0
    try:
        safety = service.restore(args.file, confirm=True)
    except (StorageError, ValidationError) as exc:
        out.error(str(exc))
        return 1
    out.success(f"Restored from {args.file}")
    out.info(f"Safety backup: {safety}")
    return 0


# --------------------------------------------------------------------------- #
# Argument parser construction
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lilyverse",
        description="LilyVerse — The Eternal Bloom Timeline (unofficial Cookie Run fan project)",
    )
    parser.add_argument(
        "--no-rich",
        action="store_true",
        help="Disable Rich styling even if installed.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common_flags(p):
        p.add_argument("--no-rich", action="store_true", help="Disable Rich styling.")

    # version
    p = sub.add_parser("version", help="Show LilyVerse version.")
    p.set_defaults(func=cmd_version)

    # dashboard
    p = sub.add_parser("dashboard", help="Show the LilyVerse dashboard.")
    p.set_defaults(func=cmd_dashboard)

    # timeline list
    p = sub.add_parser("timeline", help="Timeline management.")
    tsub = p.add_subparsers(dest="timeline_action", required=True)

    p_list = tsub.add_parser("list", help="List milestones.")
    p_list.add_argument("--character", help="Filter by character.")
    p_list.add_argument("--category", help="Filter by category.")
    p_list.add_argument("--sort", choices=["oldest", "newest"], default="oldest", help="Sort order.")
    p_list.add_argument("--search", help="Search keyword.")
    p_list.set_defaults(func=cmd_timeline_list)

    p_show = tsub.add_parser("show", help="Show a milestone by ID.")
    p_show.add_argument("id", help="Milestone ID.")
    p_show.set_defaults(func=cmd_timeline_show)

    p_add = tsub.add_parser("add", help="Add a milestone.")
    p_add.add_argument("--title", default="")
    p_add.add_argument("--date", default="", help="ISO date YYYY-MM-DD.")
    p_add.add_argument("--character", default="")
    p_add.add_argument("--category", default="")
    p_add.add_argument("--entry-type", default="", dest="entry_type")
    p_add.add_argument("--description", default="")
    p_add.add_argument("--source", default="")
    p_add.add_argument("--interactive", action="store_true", help="Prompt for missing fields.")
    p_add.set_defaults(func=cmd_timeline_add)

    p_search = tsub.add_parser("search", help="Search milestones by keyword.")
    p_search.add_argument("query", help="Search keyword.")
    p_search.set_defaults(func=cmd_timeline_search)

    p_edit = tsub.add_parser("edit", help="Edit a milestone by ID.")
    p_edit.add_argument("id", help="Milestone ID.")
    p_edit.add_argument("--title", default="")
    p_edit.add_argument("--date", default="")
    p_edit.add_argument("--character", default="")
    p_edit.add_argument("--category", default="")
    p_edit.add_argument("--entry-type", default="", dest="entry_type")
    p_edit.add_argument("--description", default="")
    p_edit.add_argument("--source", default="")
    p_edit.add_argument("--interactive", action="store_true", help="Prompt for values.")
    p_edit.set_defaults(func=cmd_timeline_edit)

    p_delete = tsub.add_parser("delete", help="Delete a milestone by ID.")
    p_delete.add_argument("id", help="Milestone ID.")
    p_delete.add_argument("--yes", action="store_true", help="Skip confirmation prompt.")
    p_delete.set_defaults(func=cmd_timeline_delete)

    # characters list
    p = sub.add_parser("characters", help="Character archive management.")
    csub = p.add_subparsers(dest="characters_action", required=True)
    p_clist = csub.add_parser("list", help="List character profiles.")
    p_clist.set_defaults(func=cmd_characters_list)
    p_cshow = csub.add_parser("show", help="Show a character profile.")
    p_cshow.add_argument("name", help="Character name.")
    p_cshow.set_defaults(func=cmd_characters_show)

    # memories list
    p = sub.add_parser("memories", help="PLA memories.")
    msub = p.add_subparsers(dest="memories_action", required=True)
    p_mem_list = msub.add_parser("list", help="List PLA trio memories.")
    p_mem_list.set_defaults(func=cmd_memories_list)

    # stats
    p = sub.add_parser("stats", help="Show timeline statistics.")
    p.set_defaults(func=cmd_stats)

    # web
    p = sub.add_parser("web", help="Start the Flask website.")
    p.set_defaults(func=cmd_web)

    # backup
    p = sub.add_parser("backup", help="Back up timeline data.")
    p.add_argument("file", nargs="?", default=None, help="Backup file path (default: timestamped in backups/).")
    p.set_defaults(func=cmd_backup)

    # restore
    p = sub.add_parser("restore", help="Restore timeline data from a backup.")
    p.add_argument("file", help="Backup file path.")
    p.add_argument("--yes", action="store_true", help="Skip confirmation prompt.")
    p.set_defaults(func=cmd_restore)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    use_rich = not getattr(args, "no_rich", False)
    out = _Output(use_rich=use_rich)

    storage = TimelineStorage()
    service = LilyVerseService(storage)

    try:
        return args.func(args, out, service)
    except (ValidationError, StorageError) as exc:
        out.error(str(exc))
        return 1
    except KeyboardInterrupt:
        out.info("Interrupted.")
        return 130

