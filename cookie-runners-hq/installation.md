# Installation Guide — Cookie Runners HQ

Cookie Runners HQ is a Flask web application with a SQLite database. No build step is required.

## Prerequisites

- Python 3.14+
- `uv` (recommended) or `pip`
- A terminal (Termux on Android works; tested on Android 14 / Termux)

## 1. Get the code

```bash
cd /path/to/CookieRunners-Everlasting-Kingdom/cookie-runners-hq
```

## 2. Create a virtual environment and install dependencies

```bash
uv venv .venv
uv pip install --python .venv -r requirements.txt
```

This installs Flask, Werkzeug and python-dotenv.

## 3. Configure environment variables

Copy the example file and edit it:

```bash
cp .env.example .env
```

Then open `.env` and set at minimum:

```text
SECRET_KEY=<a long random string>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<choose a strong password>
```

Optional:

```text
CRU_DATABASE_PATH=/absolute/path/to/cookie_runners_hq.db
PORT=5000
FLASK_ENV=development
```

**Never commit `.env`.** It is gitignored.

## 4. Initialize the database and run

The database schema and seed data are created automatically on first run:

```bash
.venv/bin/python app.py
```

Open <http://localhost:5000> (or the printed URL).

## 5. First admin login

Go to <http://localhost:5000/admin/login> and sign in with the username/password from `.env`. The admin dashboard lets you:

- Add, edit and remove games
- Publish, edit and remove announcements (with confirmation levels)
- Add game updates and maintenance notices
- Add in-game events
- Manage calendar items
- Manage news categories

Change the default admin password immediately.

## Resetting the database

The SQLite database file is created next to the app (or at `CRU_DATABASE_PATH`). To start fresh, stop the app, delete the `.db` file, and restart — seed data will be recreated.

## Production notes

- The built-in Flask server is for development only. For production, serve `app:app` with a WSGI server such as gunicorn.
- Set a strong, unique `SECRET_KEY`.
- Use HTTPS and keep `ADMIN_PASSWORD` strong.
- Never store API keys or secrets in the repository; none are required to run the app.

## Troubleshooting

**Werkzeug debug reloader crashes on import (`_PyType_AllocNoTrack`).**
This is a known incompatibility of the Werkzeug reloader with certain Python 3.14 builds (e.g. some Termux environments). The app runs correctly with `debug=False` (the default in `app.py` when run directly).

**Routes return 404.**
Make sure you started the app from the `cookie-runners-hq` folder so `templates/` and `static/` are found.

**Tests**
Run the Flask test-client suite:

```bash
.venv/bin/python tests/smoke_test.py
```
