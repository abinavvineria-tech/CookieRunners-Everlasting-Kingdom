# CookieVerse Eternal Ceremony — The Eternal Legends Edition

Unofficial, fan-made Cookie Run celebration built with **Python Flask**, HTML5, CSS3, and vanilla JavaScript.

> Tagline: *“One CookieVerse. Many legends. One unforgettable celebration.”*

## What this is

A mobile-friendly awards-night ceremony website that celebrates Cookie Run games, legendary characters, memorable updates, and the worldwide Cookie Runners community. Every award category and winner is **fan-selected** — none of these are official Devsisters awards.

### Awards featured
1. Legend of the Game Award — White Lily Cookie and Mogra Cookie
2. Best Update Award — Cookie Run: Kingdom (CRK)
3. Best Original Game Award — Cookie Run: OvenBreak (10th anniversary: 27 October 2016 → 27 October 2026)
4. Friendship & Teamwork Award — All Cookie Runners
5. Dragon Legend Award — The legendary Dragon Cookies
6. Best Villain Award — Shadow Milk Cookie
7. Eternal Memory Award — White Lily Cookie
8. Special Flower Legend Award — Mogra Cookie
9. CookieVerse Legacy Award — Every Cookie Run game
10. Lifetime Achievement Award — Devsisters and the teams behind Cookie Run

## Project structure

```
final_ceremony_ending/
├── app.py                 # Flask backend (serves the ceremony)
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── templates/
│   └── ceremony.html      # Ceremony HTML template
└── static/
    ├── style.css          # Theme, animations, responsive layout
    └── ceremony.js        # Vanilla JS ceremony interactions
```

No database, no paid APIs, no API keys, no mandatory external services. The core ceremony works entirely client-side once the page loads.

## Run on Termux (Android)

1. Open Termux and make sure packages are up to date:
   ```bash
   pkg update && pkg upgrade
   pkg install python
   ```
2. Navigate to the project folder:
   ```bash
   cd ~/Projects/crk_project/final_ceremony_ending
   ```
3. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your Android browser (Chrome, Firefox, etc.).

To access from another device on the same Wi-Fi, use the host device's local IP address and port `5000` (e.g. `http://192.168.1.23:5000`). Do not expose the Flask development server directly to the public internet without suitable production hosting and a security review.

## Run on Ubuntu

1. Open a terminal in the project folder:
   ```bash
   cd ~/Projects/crk_project/final_ceremony_ending
   ```
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.

## Testing checklist

Before declaring the ceremony complete, verify each of the following:

- [ ] Flask app starts and the home/welcome screen loads.
- [ ] “Begin the Eternal Ceremony” button starts the ceremony.
- [ ] Each award title animates before its winner is revealed.
- [ ] Next Award moves forward through all 10 awards.
- [ ] Previous Award moves backward.
- [ ] Skip to Finale jumps straight to the finale.
- [ ] Ceremony progress shows “Award X of 10”.
- [ ] Finale displays all major winners and the finale message.
- [ ] Replay Ceremony returns to the welcome screen.
- [ ] Copy Ceremony Summary copies winners + categories to the clipboard.
- [ ] All buttons work on Android mobile browsers and desktop browsers.
- [ ] Responsive layout works in portrait and landscape (no horizontal overflow).
- [ ] Reduced-motion preference disables animations/transitions.
- [ ] No JavaScript errors in the browser console.
- [ ] Fan-project disclaimer is visible in the footer.

## Accessibility

- Skip-to-ceremony link for keyboard users.
- Visible focus indicators on all interactive controls.
- ARIA labels on buttons and award regions.
- `aria-live` progress announcement.
- `prefers-reduced-motion` support disables animations and sparkles.
- Touch-friendly buttons sized for Android phones and tablets.

## Unofficial fan-project disclaimer

> This is an unofficial, fan-made Cookie Run celebration created by Cookie Runners for entertainment and community appreciation. It is not affiliated with, endorsed by, or sponsored by Devsisters. All award categories and winners presented here are fan-selected. Cookie Run names and related intellectual property belong to their respective owners.

The disclaimer appears in the page footer and is rendered from the backend so it cannot be accidentally removed by client-only changes.

## Notes

- The live date/time, when shown, is labelled Asia/Kolkata only (no external timezone library required).
- Background stars and sparkles use pure CSS — no image assets required.
- No copyrighted character artwork is assumed to be available locally; all medals/icons are emoji or CSS-drawn.
