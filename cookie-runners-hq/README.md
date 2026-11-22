# Cookie Runners HQ

**"One community. Every cookie. Infinite adventures."**

Cookie Runners HQ is a community-made information hub for Cookie Run fans. It tracks, organizes and displays Cookie Run announcements, game updates, upcoming games, events and news — with a clear separation between **confirmed** Devsisters announcements, **rumours** and **speculation**.

Built by Captain Abinav and the Cookie Runners United (CRU) family. Not an official Devsisters product. No official Cookie Run artwork is used.

## Features

1. **Dashboard** — latest announcements, upcoming releases, recent updates, current/upcoming events, featured games, community news and a verification note.
2. **Games Directory** — CookieRun: Kingdom, CookieRun: OvenBreak, CookieRun: Tower of Adventures, CookieRun: Witch's Castle and other titles, each with its own page (description, release date, platforms, updates, events, official links, development status).
3. **Devsisters Update Tracker** — announcements filterable by category, type and confirmation level (confirmed / rumour / speculation). Rumours are never presented as official news.
4. **Upcoming Games Tracker** — officially announced / in development / release date announced / released / unconfirmed-rumoured statuses.
5. **Update Calendar** — monthly and weekly views of launches, updates, maintenance, events, anniversaries and developer announcements.
6. **Admin Dashboard** — password-protected administration: add/edit/remove games, announcements, updates, events, calendar items and news categories. Session-based authentication with access controls.
7. **API** — JSON endpoints: `/api/games`, `/api/announcements`, `/api/events`, `/api/calendar`.
8. **Design** — premium Cookie Run-inspired fantasy interface: magical-kingdom atmosphere, cookie-themed gradients, rounded cards, smooth animations, mobile-first responsive layout, dark and light themes.
9. **States** — loading, empty and error states throughout; search and filtering on all list pages.

## Tech stack

- Python 3.14 + Flask 3
- SQLite database (file-based, configured via `CRU_DATABASE_PATH`)
- Werkzeug password hashing + Flask session authentication
- Vanilla CSS/JavaScript (no build step, no frontend framework)
- `python-dotenv` for environment configuration

## Installation & quick start

See `installation.md` for the full guide. In short:

```bash
# 1. Clone / open the cookie-runners-hq folder
cd cookie-runners-hq

# 2. Create a virtual environment and install dependencies
uv venv .venv
uv pip install --python .venv -r requirements.txt

# 3. Configure environment
cp .env.example .env
# edit .env: set SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD

# 4. Run
.venv/bin/python app.py
# open http://localhost:5000
```

Default admin login (change immediately in production): `admin` / the password you set in `.env` (`ADMIN_PASSWORD`).

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `SECRET_KEY` | `dev-secret-change-me-in-production` | Flask session signing |
| `ADMIN_USERNAME` | `admin` | Admin account username |
| `ADMIN_PASSWORD` | `changeme-admin-123` | Admin account password (change this!) |
| `CRU_DATABASE_PATH` | `<project>/cookie_runners_hq.db` | SQLite database file path |
| `PORT` | `5000` | Dev server port |

Never commit `.env`. API keys/secrets are never stored in the repository.

## Project structure

```
cookie-runners-hq/
  app.py                 # Flask app factory, routes, admin auth
  database.py            # SQLite schema, seed data, queries
  requirements.txt       # Python dependencies
  .env.example           # Environment variable template (copy to .env)
  .gitignore
  tests/smoke_test.py    # Flask test-client smoke tests
  static/css/style.css   # Design system (Cookie Run fantasy theme, dark/light)
  static/js/app.js       # Theme toggle, mobile nav, flash dismiss, delete confirm
  templates/             # Jinja2 pages (base, dashboard, games, tracker, calendar, admin, ...)
```

## Confirmation levels (rumour vs speculation policy)

Every announcement, update, event and calendar item carries a confirmation level:

- **Confirmed** — matched to a public official source where one is provided.
- **Rumour** — unverified report; not official news.
- **Speculation** — community speculation; not official news.

Cookie Runners HQ never presents rumours or speculation as confirmed Devsisters announcements. Where automatic Devsisters feeds or APIs are unavailable, entries are published manually through the admin dashboard, and each entry can cite its source URL.

## Testing

Run the Flask test-client smoke suite (public pages, admin login/CRUD, confirmation labels, seeding):

```bash
.venv/bin/python tests/smoke_test.py
```

Result (verified): all checks passed — dashboard, games directory, game detail, tracker, upcoming games, calendar (month + week), search, JSON APIs, admin login protection, add/edit/delete for games, announcements, updates, events, calendar items and categories, plus 404 handling.

## GitHub issue

This project resolves repository issue **#6** ("create an cookie runners project" — "create an new project by the given chatgpt prompt :)").

## License / attribution

Fan-made project for the Cookie Run community. Cookie Run and related trademarks belong to Devsisters Corporation. This site is not affiliated with or endorsed by Devsisters.
