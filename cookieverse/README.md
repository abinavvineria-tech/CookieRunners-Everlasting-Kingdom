# Cookie Runners Golden Ballon d'Or 2026

## Official Fan Project

**Name:** COOKIE RUNNERS GOLDEN BALLON D'OR  
**Edition:** First Edition — 2026  
**Tagline:** "Every Cookie. Every Legend. One Golden Legacy."  
**Motto:** "United by Cookies. Remembered by Legends."

## Disclaimer

This is an **unofficial community-created fan project** celebrating Cookie Run characters, stories, and communities. Not affiliated with, endorsed by, or sponsored by Devsisters Corp. Cookie Run: Kingdom, Cookie Run: OvenBreak, CookieRun: OvenSmash, and all related trademarks belong to their respective owners.

## Features

- Premium gold and midnight visual design
- Interactive ceremony with confetti, spotlight, and reveal sequence
- 15 award categories (Golden Ballon d'Or, Golden Heart, Golden Teammate, Golden Legend, Rising Star, Best Guardian, Best Villain, Best Duo, Best Friendship, Golden Leadership, Best Teammate, Eternal Legacy, Golden Memory, Best Cookie Run Game, Best Update, Community Award, Creative Cookie Runner, Lifetime Achievement)
- First Edition predefined winners preserved (White Lily Cookie, Mogra Cookie, Pure Vanilla Cookie)
- Admin dashboard with authentication, winner management, export (JSON/CSV)
- Nomination center
- Hall of Fame timeline
- CLI companion `cr-golden`
- Responsive mobile-first layout
- SQLite persistence

## Installation

```bash
python3 -m venv venv
source venv/bin/activate  # Termux: source venv/bin/activate
pip install -r requirements.txt
```

## Launch

```bash
python app.py
```

Visit `http://localhost:5000`.

## CLI

```bash
python scripts/cr_golden.py ceremony
python scripts/cr_golden.py winners
python scripts/cr_golden.py awards
python scripts/cr_golden.py history
python scripts/cr_golden.py nominees
python scripts/cr_golden.py version
```

Or via the wrapper:

```bash
./cr-golden ceremony
```

## Admin Login

Username: `cookie-runners-admin`  
Password: `golden-ball-2026`

Navigate to `/admin/login` after launching the app.

## Project Structure

```
cookie-runners-golden-ballon-dor/
  app.py
  database.py
  routes.py
  requirements.txt
  README.md
  templates/
  static/css/style.css
  static/js/app.js
  static/images/
  scripts/cr_golden.py
  cr-golden
```

## Deployment

- Native Android Termux (Python 3 + Flask available)
- Ubuntu / Linux
- Localhost development (`python app.py`)
- Production: set environment variables and use a WSGI server.

## First Edition Winners (Protected)

- Golden Ballon d'Or — White Lily Cookie, Mogra Cookie
- Golden Heart Award — White Lily Cookie, Mogra Cookie
- Golden Teammate Award — Pure Vanilla Cookie
