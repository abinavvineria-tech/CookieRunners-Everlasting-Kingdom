# Champions League Countdown Nexus

**Champions League Countdown Nexus** is a live countdown companion application for the Cookie Run: Kingdom Champions League Welcome Night.

> **Unofficial fan project — not an official Devsisters website.**
> Not affiliated with or endorsed by Devsisters. All franchise references belong to their respective owners.

## Event
- **Event:** Cookie Run Kingdom Champions League Welcome Night
- **Date:** 18 November 2026
- **Kickoff:** 8:30 PM IST (Asia/Kolkata)
- **Theme:** Emerald green & midnight forest with gold championship accents

## Features
1. Live countdown synchronized with the system clock.
2. Accurate Asia/Kolkata (IST) timezone handling via zoneinfo.
3. Automatic transition to an event-started screen when the countdown reaches zero.
4. Event information dashboard (name, datetime, timezone, status, description).
5. Copy and share event details (Clipboard API + Web Share API).
6. Persistent event configuration (stored in data/events.json, editable without code changes).
7. Optional browser notifications requested only with explicit user consent.
8. Accessible controls and responsive mobile-first layouts.

## Visual identity
- Emerald green (#10b981) and midnight forest (#0a1610) backgrounds.
- Elegant gold championship accents (#d4af37).
- Botanical fantasy atmosphere with subtle gradient glows.
- Premium serif + sans-serif typography.
- Responsive mobile-first interface.

## Project structure
champions-league-countdown-nexus/
├── run.py
├── requirements.txt
├── README.md
├── config.py
├── data/events.json
├── app/__init__.py
├── app/app.py
├── templates/index.html
├── static/css/style.css
├── static/js/app.js
├── tests/test_countdown.py
└── docs/hermes-integration.md

## Backend (Flask)
- GET / serves the countdown frontend.
- GET /api/event returns event config + computed countdown state (never hardcoded).
- POST /api/event validates + persists updated event configuration.
- GET /api/health health check.

Countdown calculations derive the target from data/events.json (date + time + timezone). The value is never hardcoded.

## Setup (Termux / Android)

cd ~/Projects/crk_Projects/champions-league-countdown-nexus
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 run.py

Open http://127.0.0.1:5000 (or http://<your-phone-ip>:5000 from another device on LAN).

Environment variables:
SECRET_KEY (default dev-secret-change-me)
DEBUG (default true)
HOST (default 0.0.0.0)
PORT (default 5000)
PERSIST_EVENTS (default true)

Never commit real secrets. SECRET_KEY is read from the environment.

## Tests
source .venv/bin/activate
python -m pytest tests/ -v
# or: python -m unittest tests.test_countdown -v

Tests cover countdown accuracy, event transitions, input validation, and the health endpoint.

## Frontend
HTML5, CSS3, vanilla JavaScript. No build step required.
- Countdown ticks every second, synchronized with the system clock.
- Automatic switch to the event started overlay at zero.
- Notification permission requested only on user click (consent-only).
- Copy to clipboard and native share fallbacks.
- Dark/light theme toggle persisted in localStorage.
- ARIA labels, skip link, keyboard navigation, reduced-motion support.

## Accessibility
Skip-to-content link, ARIA labels, keyboard-navigable menu and buttons, prefers-reduced-motion honored, focus-visible styles.

## License
Fan project for personal/educational use. No commercial affiliation implied.
