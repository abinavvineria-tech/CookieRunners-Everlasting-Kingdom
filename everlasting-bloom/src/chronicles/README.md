# CookieVerse Chronicles — Setup & Launch Guide

Unofficial fan-made archive. Not affiliated with or endorsed by Devsisters.

## Requirements
- Python 3.10+ (tested on Python 3.12 on Android Termux / Ubuntu)
- No external dependencies beyond standard library + Flask

## Install

```bash
cd ~/Projects/crk_project/everlasting-bloom/src/chronicles
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Initialize database

The `app.py` initializes SQLite automatically when started. If you want to seed it manually:

```bash
python3 -c "from app import app, init_schema; app.app_context().push(); init_schema()"
```

## Launch

```bash
python3 app.py
```

The server listens on `0.0.0.0:5000`. On Termux / Android browsers, visit `http://localhost:5000/` (or the device's local IP if accessing from another machine on the same network).

## Verify

```bash
python3 scripts/verify.py
```

This runs a Flask test client through routes, CSRF checks, and API endpoints.

## Design notes
- `instance/chronicles.db` holds all timeline entries (gitignored — don't commit DB files)
- `templates/` uses Jinja2 with a fantasy cookie-cream theme (gold accents, rainbow jelly gradient border on cards)
- Dark mode toggles via `localStorage` and the floating theme button
- All interactive buttons work on mobile (touch targets >= 44px, responsive grid cards)
- Every event card links to `/project/<id>`; `/add` and `/edit` forms include CSRF tokens
- Unofficial labeling is always visible: banner at top of every page + footer disclaimer
