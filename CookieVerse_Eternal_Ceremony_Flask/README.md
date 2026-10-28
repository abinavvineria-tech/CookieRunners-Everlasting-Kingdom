# CookieVerse Eternal Ceremony 🍪✦

A mobile-friendly, unofficial Cookie Run fan ceremony website built with Python Flask.

## Features
- Ceremony landing page and five-part program
- Responsive design for phones, tablets, and desktop
- Interactive celebration-light button
- Friendship oath form with working POST endpoint
- Community guestbook saved locally to `guestbook.json`
- Clear unofficial fan-project disclaimer
- No API keys or external database required

## Run on Termux or Ubuntu

1. Install Python if needed.
2. Open this project folder.
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   ```
4. Activate it:
   - Ubuntu: `source .venv/bin/activate`
   - Termux: `source .venv/bin/activate`
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Start the website:
   ```bash
   python app.py
   ```
7. Open `http://127.0.0.1:5000` in your browser.

For access from another device on the same Wi-Fi, use the host device's local IP and port `5000`. Do not expose a development server directly to the public internet without suitable production hosting and security review.

## Notes
- Guestbook entries are stored in a local JSON file and are not shared across separate deployments.
- The site uses a Google Fonts import for typography; system fallbacks are included.
- This is an unofficial fan project, not affiliated with or endorsed by Devsisters or the official Cookie Run games.
