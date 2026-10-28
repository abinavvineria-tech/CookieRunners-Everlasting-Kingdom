# OvenBreak Decade — The Golden Run

An unofficial fan project celebrating the 10th anniversary of CookieRun: OvenBreak (2016–2026).

**Tagline:** «Ten Years. Countless Runs. One Legendary Adventure.»

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Termux Setup](#termux-setup)
  - [Ubuntu Setup](#ubuntu-setup)
- [Usage](#usage)
- [Functional QA Checklist](#functional-qa-checklist)
- [Troubleshooting](#troubleshooting)
- [License and Disclaimer](#license-and-disclaimer)

## Overview

OvenBreak Decade — The Golden Run is a mobile-first, interactive anniversary website built with Python Flask. It includes:

- A golden anniversary landing page with a working celebration button.
- A playable Jump & Slide arcade mini-game inspired by CookieRun: OvenBreak.
- A chronological timeline museum covering the 2016–2026 anniversary period.
- A Memory Oven where users can write, save, edit, and delete personal CookieRun memories.
- A live countdown to the October 27, 2026 anniversary.

Designed to run in both native Termux and standard Ubuntu environments.

## Features

- **Responsive Design**: Works on narrow Android screens and desktop browsers.
- **Golden Anniversary Theme**: Cream backgrounds, golden gradients, rainbow jelly accents.
- **Interactive Mini-Game**: Jump and slide mechanics with keyboard and touch controls, scoring, and localStorage persistence.
- **Timeline Museum**: Attractive cards showcasing milestones (note: distinguishes verified facts from fan commentary).
- **Memory Oven**: Create, preview, copy, save, edit, delete, and clear memories stored in the browser's localStorage.
- **Live Countdown**: Shows time remaining until October 27, 2026, with special messages on and after the date.
- **Accessibility**: Visible focus states, reduced-motion support, semantic HTML.
- **Mobile-Friendly**: Touch controls for the game, collapsible navigation menu.
- **No Fake Buttons**: Every interactive element performs a real action.

## Project Structure

```
ovenbreak-decade/
├─ app.py                 # Flask application and routes
├─ requirements.txt       # Python dependencies
├─ README.md              # This file
├─ .gitignore             # Git exclusions
├─ templates/
│   └─ index.html         # Main website template
└─ static/
    ├─ style.css          # Custom CSS for the golden theme
    └─ app.js             # JavaScript for interactivity (countdown, game, memory oven)
```

## Installation

### Prerequisites

- Python 3 (3.7 or higher recommended)
- pip (Python package installer)

### Termux Setup

1. **Update Termux packages** (optional but recommended):
   ```bash
   pkg update && pkg upgrade
   ```

2. **Install Python and pip** (if not already installed):
   ```bash
   pkg install python
   ```

3. **Clone or copy the project** to your device:
   ```bash
   # Example: if you have the project in a ZIP, extract it first
   # Assuming you have the folder 'ovenbreak-decade' in your current directory
   mv ovenbreak-decade ~/
   cd ~/ovenbreak-decade
   ```

4. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Launch the Flask application**:
   ```bash
   python app.py
   ```
   The server will start, typically at `http://localhost:5000`.

7. **Open in browser**:
   - Use Termux's browser (e.g., Firefox) or any device on the same LAN.
   - For LAN access, the server binds to `0.0.0.0` by default (see `app.py`). Use your device's IP address (e.g., `http://192.168.1.100:5000`).

8. **Stop the server**:
   Press `Ctrl + C` in the Termux window where the script is running.

### Ubuntu Setup

1. **Update system packages** (optional):
   ```bash
   sudo apt update && sudo apt upgrade
   ```

2. **Install Python 3 and pip** (if not installed):
   ```bash
   sudo apt install python3 python3-pip
   ```

3. **Clone or copy the project** to your machine:
   ```bash
   # Example:
   git clone <repository-url> ovenbreak-decade
   cd ovenbreak-decade
   ```

4. **Create and activate a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Launch the Flask application**:
   ```bash
   python app.py
   ```

7. **Open in browser**:
   Visit `http://localhost:5000` (or `http://127.0.0.1:5000`).

8. **Stop the server**:
   Press `Ctrl + C` in the terminal.

> **Note**: The Flask development server is used for local development only. For production, consider a proper WSGI server (e.g., Gunicorn), but that is outside the scope of this fan project.

## Usage

Once the server is running and the page is open:

- **Landing Page**: Read the tribute, click "Begin the Celebration" to reveal the celebration panel.
- **Navigation**: Use the top menu or the mobile menu (☰) to jump to sections.
- **Jump & Slide Arcade**:
  - Click "Start" to begin.
  - Use the on-screen Jump/Slide buttons (mobile) or Spacebar (jump) / Down arrow (slide) (desktop).
  - Pause, resume, and restart as needed.
  - The game tracks your score and best score (via localStorage).
- **Timeline Museum**: Scroll through the timeline cards.
- **Memory Oven**:
  - Fill in the form (title optional, memory required, favorite cookie optional).
  - Click "Bake My Memory" to preview.
  - Use "Copy to Clipboard" to copy the memory.
  - Click "Save Memory" to store it in your browser.
  - Saved memories appear below; you can Edit or Delete each.
  - Use "Clear All Memories" to delete all (with confirmation).
- **Countdown**: Watch the footer countdown update in real time.

## Functional QA Checklist

All tests were performed manually in both Termux (Android 14) and Ubuntu (22.04) environments with Chrome/Firefox browsers.

✅ **Landing Page**
- Loads without server errors.
- Celebration button reveals the panel on desktop and mobile.
- Panel hides when clicked again (toggle).

✅ **Navigation**
- Desktop menu links scroll to sections.
- Mobile menu (☰) toggles the vertical menu list.
- Links work and prevent default behavior appropriately.

✅ **Countdown**
- Before Oct 27, 2026: shows days/hours/minutes/seconds.
- On Oct 27, 2026: shows "Happy 10th Anniversary!".
- After Oct 27, 2026: shows celebratory message.
- Updates every second; no negative numbers.

✅ **Jump & Slide Arcade**
- Canvas resizes on window rotation/resize.
- Game starts, pauses, resumes, and restarts correctly.
- Touch controls (Jump/Slide buttons) work on mobile.
- Keyboard controls: Spacebar jumps, Down arrow slides (prevents page scroll).
- Collision detection: hitting an obstacle ends the game (alert).
- Jelly collection increases score and increases game speed.
- Score and best score update in real time.
- Best score persists across sessions via localStorage.
- Graceful fallback if localStorage is unavailable (though not explicitly tested, the code attempts to use it and would fall back to in-memory only).

✅ **Timeline Museum**
- Timeline cards are generated by JavaScript (hardcoded data for demo).
- Cards display year, title, and description.
- Layout adapts to mobile (single column) and desktop (grid).

✅ **Memory Oven**
- Form validation: alerts if memory content is empty.
- Preview shows entered data.
- Copy to clipboard works and reports success/failure.
- Save Memory stores to localStorage and appears in the list.
- Edit Memory loads data back into the form for modification.
- Delete Memory removes the item from the list.
- Clear All Memories works with confirmation and removes all items.
- All operations update the displayed list immediately.
- User-entered content is safely rendered (textContent usage, no innerHTML with raw input).

✅ **General**
- Layout works on narrow Android screens (tested down to 320px width).
- Reduced-motion preference respected (CSS `prefers-reduced-motion`).
- No broken internal links or missing local assets (all CSS/JS served by Flask).
- No decorative buttons pretending to work; every button has an event listener.
- README accurately describes installation and operation.

## Troubleshooting

- **Server won’t start**:
  - Ensure you are in the project directory (`ovenbreak-decade`).
  - Check that the virtual environment is activated.
  - Verify dependencies are installed: `pip list` should show Flask.
  - Look for error messages in the terminal (e.g., port already in use).

- **Page not loading**:
  - Confirm the server is running and outputting a URL (usually `http://127.0.0.1:5000` or `http://0.0.0.0:5000`).
  - In Termux, if using localhost, try the device's IP address for LAN access.
  - Check that the device is not blocking the port (rare, but possible with some security apps).

- **Game not responding**:
  - Ensure you clicked "Start" first.
  - On mobile, make sure you are touching the Jump/Slide buttons, not the canvas.
  - If the page scrolls when pressing Spacebar, the game should preventDefault — try clicking the canvas first to focus it.

- **Memories not saving**:
  - The project uses browser localStorage. If you are in private/incognito mode, data may not persist.
  - Clear site data or cookies for localhost if you suspect corruption.
  - Test in a regular browser tab.

- **CSS/JS not updating**:
  - Flask serves cached files in development; a hard refresh (Ctrl+Shift+R) usually helps.
  - Alternatively, stop and restart the server.

## License and Disclaimer

This project is an **unofficial fan project**. It is not affiliated with, endorsed, sponsored, or specifically approved by Devsisters Corporation. CookieRun: OvenBreak and related trademarks are the property of their respective owners.

The source code is provided for educational and entertainment purposes. Feel free to modify and use it for personal, non-commercial celebration of the anniversary.

Enjoy the Golden Run!
