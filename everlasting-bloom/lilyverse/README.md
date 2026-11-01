# LilyVerse — The Eternal Bloom Timeline

**Tagline:** “One Lily. Countless Memories. An Eternal Bloom.”

An unofficial Cookie Run fan project combining a beautiful Flask website with a
powerful command-line interface (CLI). Both interfaces share one JSON data
store, so your timeline is always consistent whether you manage it from the
browser or the terminal.

Celebrates White Lily Cookie, Pure Vanilla Cookie, Mogra Cookie, the PLA trio
(Pure Vanilla, Lily, and Abinav), and your personal Cookie Run journey.

> **Unofficial fan project.** Not affiliated with or endorsed by Devsisters.
> Cookie Run, Cookie Run: Kingdom, Cookie Run: OvenBreak, White Lily Cookie,
> Pure Vanilla Cookie, Mogra Cookie and related names are trademarks of their
> respective owners. Official game facts are clearly separated from personal
> memories and fan interpretations.

---

## Features

- **Flask website** — mobile-first, responsive, light/dark mode, animated
  glassmorphism, accessible keyboard navigation, reduced-motion support.
- **Home** — hero with tagline, working buttons, bloom stats, recent memories.
- **Character Archives** — White Lily Cookie, Pure Vanilla Cookie, Mogra
  Cookie, and your Cookie Run journey (biographies + associated milestones).
- **Interactive Timeline** — chronological cards, search, filter by
  character/category, sort newest/oldest, expandable details, date/source
  labels, add/edit/delete via validated forms.
- **PLA Memories** — shared timeline for Pure Vanilla Cookie, White Lily Cookie,
  and Abinav, with character introductions, reflections, and a three-part
  visual layout.
- **Eternal Memory Garden** — respectful White Lily remembrance page,
  session-based flower-offering counter, tribute message, memory gallery, and
  visitor messages with validation.
- **CLI** (`lilyverse` / `python -m lilyverse`) — full timeline, character,
  memory, stats, backup, restore, and website management.
- **Shared JSON storage** — atomic writes (temp file + `os.replace`), file
  locking (`fcntl`), input validation, undated memories, stable unique IDs.
- **Tests** — `unittest`-based automated test suite.
- **No paid services or mandatory API keys.** Runs on Android Termux and
  Ubuntu Linux.

---

## Project Structure

```
lilyverse/
├── app.py                    # Flask dev entry point
├── requirements.txt          # Runtime deps (Flask only)
├── pyproject.toml            # Packaging metadata
├── README.md                 # This file
├── LICENSE                   # MIT
├── lilyverse/                # Python package
│   ├── __init__.py           # Package metadata (__version__ = 1.0.0)
│   ├── __main__.py           # python -m lilyverse entry point
│   ├── cli.py                # argparse CLI (all commands)
│   ├── models.py             # Data models + validation
│   ├── storage.py            # JSON storage + atomic writes + locking + backup/restore
│   ├── services.py           # Shared business logic (CLI + Flask)
│   └── web.py                # Flask app factory + routes
├── templates/                # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── timeline.html
│   ├── timeline_detail.html
│   ├── timeline_add.html
│   ├── timeline_edit.html
│   ├── characters.html
│   ├── character_detail.html
│   ├── pla.html
│   ├── memories.html
│   └── error.html
├── static/
│   ├── css/style.css         # Responsive, light/dark, accessibility
│   └── js/main.js            # Nav, theme toggle, confirm dialogs
├── data/                     # JSON data store (created on first run)
│   └── timeline.json
├── backups/                  # Timestamped JSON backups
└── tests/                    # unittest test suite
    ├── test_cli.py
    ├── test_storage.py
    └── test_web.py
```

---

## Installation

### Prerequisites

Python 3.9+ (tested on Python 3.14 under Termux/Android 14).

### Termux (Android)

1. Install Python and git if you haven't:
   ```
   pkg install python git
   ```
2. Clone or place the project in your workspace:
   ```
   cd ~/Projects/crk_project/everlasting-bloom/lilyverse
   ```
3. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```
4. Install dependencies and the package in editable mode:
   ```
   python -m pip install -r requirements.txt
   python -m pip install -e .
   ```

### Ubuntu Linux

Same steps as above, using `python3` and `python3 -m venv` if your system
distinguishes them:
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
```

> On Termux, `python` and `python3` point to the same interpreter after the
> `python` package is installed. The `lilyverse` console script is installed
> into `.venv/bin/lilyverse` (on your PATH when the venv is active).

---

## Usage

### Start the website

From the `lilyverse` project root (with the venv active):

```
python app.py
```

Open `http://127.0.0.1:5000` in your local browser.

Configuration via environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `LILYVERSE_HOST` | `127.0.0.1` | Bind host (dev server, local only) |
| `LILYVERSE_PORT` | `5000` | Bind port |
| `LILYVERSE_DEBUG` | `0` | Set `1` to enable Flask debug (development only) |
| `LILYVERSE_SECRET_KEY` | random | Flask session secret |

**Security:** Debug mode is disabled by default. Do not expose the Flask
development server to the public internet. For safe LAN access, bind to your
LAN IP (`LILYVERSE_HOST=0.0.0.0`) only within a trusted private network and
never expose port 5000 to the internet.

### Use the CLI

With the venv active:

```
lilyverse --help
lilyverse dashboard
lilyverse timeline list
```

Or without installing the package globally:

```
python -m lilyverse --help
python -m lilyverse dashboard
python -m lilyverse timeline list
```

Rich terminal styling is used automatically when the `rich` package is
installed (`pip install rich`); otherwise a clean plain-text fallback is used.

### Required CLI commands

```
python -m lilyverse --help
python -m lilyverse dashboard
python -m lilyverse timeline list
python -m lilyverse timeline list --character "White Lily Cookie"
python -m lilyverse timeline list --sort newest
python -m lilyverse timeline show <ID>
python -m lilyverse timeline add
python -m lilyverse timeline search "White Lily"
python -m lilyverse timeline edit <ID>
python -m lilyverse timeline delete <ID>
python -m lilyverse characters list
python -m lilyverse characters show "Mogra Cookie"
python -m lilyverse memories list
python -m lilyverse stats
python -m lilyverse web
python -m lilyverse backup
python -m lilyverse restore <BACKUP_FILE>
python -m lilyverse version
```

**Interactive commands** (`timeline add`, `timeline edit`) prompt for missing
information when run without the corresponding flags, while supporting flags
for automation:

```
# Interactive add (prompts for each field)
python -m lilyverse timeline add

# Automated add with flags
python -m lilyverse timeline add --title "My milestone" --date 2026-11-01 \
  --character "Abinav" --category personal --entry-type "personal memory" \
  --source personal --description "A new memory."

# Delete with confirmation skipped (use with care)
python -m lilyverse timeline delete <ID> --yes
```

---

## Data Model

One shared JSON file (`data/timeline.json`). Each milestone has:

| Field | Type | Notes |
|---|---|---|
| `id` | string | Stable unique ID (auto-generated from title) |
| `title` | string | Required |
| `date` | string \| null | ISO `YYYY-MM-DD`; null = undated |
| `character` | string | Required (e.g. "White Lily Cookie", "Abinav") |
| `category` | string | Required (e.g. "personal", "milestone", "franchise") |
| `entry_type` | string | `official fact` \| `personal memory` \| `fan interpretation` |
| `description` | string | Optional |
| `source` | string | `official` \| `personal` \| `fan` |
| `created_at` | string | ISO timestamp |
| `updated_at` | string | ISO timestamp |

Custom personal characters or journey categories can be added through the CLI
or web forms without editing source code.

---

## Backup & Restore

```
# Back up to a timestamped file in backups/
python -m lilyverse backup

# Back up to a specific path
python -m lilyverse backup /path/to/my-backup.json

# Restore (prompts for confirmation; keeps a safety backup first)
python -m lilyverse restore backups/timeline-20261029T....json

# Restore without confirmation
python -m lilyverse restore backups/timeline-....json --yes
```

- Validates backup structure before restoring.
- Rejects invalid JSON and malformed records.
- Keeps a safety backup of current data before replacement.
- Never writes outside the project `data/` and `backups/` directories.

---

## Testing

Run the automated test suite (unittest):

```
python -m pytest tests/
```

Or, if pytest is unavailable, run the modules directly:

```
python -m unittest discover -s tests -v
```

Tests cover CLI help and commands, add/edit/search/delete, JSON validation,
backup/restore, shared data consistency between Flask and CLI, website routes,
form validation, invalid input, missing files, and empty-record behavior.

---

## Sample Data & Verified Facts

The included `data/timeline.json` contains sample milestones. Each record's
`entry_type` and `source` fields distinguish:

- **official fact** / `official` — verified game information (e.g. OvenBreak
  release 2016-10-27, Kingdom launch 2021-01-21).
- **personal memory** / `personal` — your own journey and achievements.
- **fan interpretation** / `fan` — fan-created content, clearly not official.

Dates from user-provided fan references (e.g. the original Cookie Run date
2009-06-12) are labeled as such and should be verified against official
archives before quoting as official release dates. No invented dialogue or
unverified announcement dates are used.

---

## Tested Commands & Limitations

**Tested commands:** `--help`, `dashboard`, `timeline list` (with
`--character`, `--category`, `--sort`, `--search`), `timeline show`, `timeline
add` (interactive + flags), `timeline search`, `timeline edit`, `timeline
delete`, `characters list`, `characters show`, `memories list`, `stats`,
`backup`, `restore`, `version`, and all Flask website routes.

**Limitations:**
- The Flask development server is single-threaded/local-only by default; use a
  production WSGI server (e.g. Waitress/Gunicorn) for anything beyond local
  use.
- File locking uses `fcntl`, which is Unix/Termux/Ubuntu-specific (matches the
  target platforms).
- The Memory Garden visitor messages and flower counter are session-based
  (stored in the Flask session), not persisted to the JSON data store.
- Rich styling is optional; plain-text fallback is fully functional.

---

## License

MIT. See `LICENSE`. This is an unofficial fan work inspired by the Cookie Run
franchise (Devsisters).
