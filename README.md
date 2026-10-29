
# Cookie Runners Everlasting Kingdom 🍪👑

**One Community. Many Adventures. An Everlasting Legacy.**

Welcome, Cookie Runners everywhere!

This is the community home for **Cookie Runners Everlasting Kingdom** — an unofficial, fan-made space celebrating Cookie Run games, characters, anniversaries, and the creativity of Cookie Runners around the world. Whether you're here for the lore, the celebrations, or the code, you belong in this kitchen.

---

## Table of Contents

- [Welcome](#welcome)
- [Project Overview & Goals](#project-overview--goals)
- [Features](#features)
- [Supported Environments](#supported-environments)
- [Installation Prerequisites](#installation-prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contribution Guidelines](#contribution-guidelines)
- [Troubleshooting & Support](#troubleshooting--support)
- [Unofficial Fan-Project Disclaimer](#unofficial-fan-project-disclaimer)

---

## Project Overview & Goals

Cookie Runners Everlasting Kingdom is a community-driven fan project dedicated to keeping the spirit of Cookie Run alive through shared celebrations, timelines, and creative experiments.

Our goals:

- Provide a welcoming front door for Cookie Runners of all experience levels.
- Document and celebrate Cookie Run milestones, including game anniversaries and community events.
- Host small, working fan creations — such as Flask-based websites, Termux tools, and Ubuntu utilities — that anyone can run and modify.
- Encourage community contributions that are honest, well-tested, and clearly labeled.

This repository is currently in a **documentation/seed stage**. The root contains this README and project documentation. Working code prototypes (for example, a Flask ceremony website) live in sibling folders within the wider workspace and are tracked separately as they mature. Nothing here is presented as a finished, installable product yet — it's a growing collection built by and for the community.

---

## Features

The following areas are the focus of this community project. Each is labeled by its current status so you know what is real and what is planned:

| Area | Description | Status |
|------|-------------|--------|
| Community fan projects | Collaborative Cookie Run celebrations and tributes created by Cookie Runners. | Active (community-led) |
| Cookie Run timelines | Community-maintained notes on game milestones and anniversaries. | In progress |
| Anniversary celebrations | Fan events marking Cookie Run anniversaries (e.g. OvenBreak's 10th year). | Planned / seasonal |
| Flask websites | Small, working Flask-based fan sites that run locally (Termux + Ubuntu). | Prototype exists in sibling workspace |
| Termux tools | Android-friendly command-line utilities for Cookie Runners on Termux. | Planned |
| Ubuntu utilities | Linux/Ubuntu command-line and desktop utilities. | Planned |
| Creative experiments | Art, writing, code experiments, and fan lore explorations. | Ongoing |

**Important:** Do not assume a feature, dependency, or application exists just because it is listed above. Only what is committed to this repository and verified to run should be considered available. If something is marked "planned" or "prototype," it is not yet part of this repo.

---

## Supported Environments

- **Android with Termux** — Python + Flask projects are designed to run in Termux on Android.
- **Linux / Ubuntu** — The same instructions apply on Ubuntu and most Linux distributions.
- **Other platforms** — Python/Flask code should run anywhere Python is supported, but mobile-first testing has focused on Android/Termux and Ubuntu.

---

## Installation Prerequisites

Before you begin, make sure you have:

- **Python 3** (3.9 or newer recommended)
- **pip** (Python's package installer)
- **git** (to clone this repository)
- A terminal: **Termux** on Android, or your regular terminal on Ubuntu/Linux

Some projects in this workspace additionally require **Flask** (see the project's `requirements.txt`). No paid APIs, API keys, or mandatory external services are needed for the core fan projects.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/abinavvineria-tech/CookieRunners-Everlasting-Kingdom.git
cd CookieRunners-Everlasting-Kingdom
```

### 2. Set up a virtual environment (recommended)

On Ubuntu / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Android Termux:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If a sub-project includes a `requirements.txt`, install it from that sub-project's folder:

```bash
pip install -r requirements.txt
```

For example, the Flask ceremony prototype uses:
```
Flask>=3.0,<4.0
```

> Note: This repository is documentation/seed stage at the root. Individual working apps live in their own folders with their own `requirements.txt`. Check each sub-project folder before installing.

### 4. Run a project

From the folder containing `app.py`:

```bash
python app.py
```

Then open your browser to `http://127.0.0.1:5000`.

For access from another device on the same Wi-Fi, use the host device's local IP address on port `5000`. Do not expose a development server directly to the public internet without suitable production hosting and a security review.

---

## Usage

- Browse the documentation in this repository to learn about the community and its projects.
- Open any sub-project folder (e.g. a Flask website) and follow its local `README.md` for setup and usage.
- Run apps locally on your Android/Termux device or Ubuntu machine.
- Remix, extend, and share your own fan creations — then contribute them back (see Contribution Guidelines).

Everything here is made for learning, celebration, and community fun. No commercial use is implied or permitted for official Cookie Run intellectual property.

---

## Contribution Guidelines

Cookie Runners Everlasting Kingdom is built by the community, for the community. Contributions are welcome!

### How to contribute

1. **Fork** the repository and create a new branch from `main`.
2. **Add or improve** documentation, code, assets, or celebration ideas.
3. **Test** your changes on Android/Termux or Ubuntu before submitting.
4. **Label clearly** any demo, prototype, or unverified feature. Do not present unofficial content as official.
5. **Open a pull request** with a clear description of what you changed and why.
6. **Be respectful** and inclusive. Cookie Runners of all backgrounds are welcome.

### What we appreciate

- Honest, working code over decorative stubs.
- Clear labels for anything unofficial, experimental, or not yet verified.
- Preservation of existing project structure and useful content.
- Fan tributes that respect Cookie Run characters and lore without inventing official dialogue or announcements.

### What to avoid

- Claiming official affiliation with Devsisters or the Cookie Run games.
- Inventing release dates, awards, or endorsements.
- Overwriting or deleting existing documentation without discussion.

---

## Troubleshooting & Support

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| `python: command not found` | Python not installed or not on PATH | Install Python 3, or on Termux: `pkg install python` |
| `pip: command not found` | pip not installed | On Termux: `pkg install python` (includes pip); on Ubuntu: `sudo apt install python3-pip` |
| `ModuleNotFoundError: No module named 'flask'` | Flask not installed | Run `pip install -r requirements.txt` from the project folder |
| Port 5000 already in use | Another app is using port 5000 | Set a different port: `FLASK_RUN_PORT=5001 python app.py` |
| App won't open on another device | Dev server bound to localhost only | Run with `host="0.0.0.0"` and use the device's local IP |
| `git clone` / push fails | Network or authentication | Check your internet connection and GitHub credentials/token |

### Getting help

- Open a **GitHub Issue** in this repository for bugs, questions, or suggestions.
- Check existing issues and discussions before posting a new one.
- Be clear about your environment (Termux/Android version, Ubuntu version, Python version) when asking for help.

This is a volunteer, fan-run community. Response times depend on contributor availability.

---

## Unofficial Fan-Project Disclaimer

**Cookie Runners Everlasting Kingdom is an unofficial, community-made fan project.**

It is **not** affiliated with, endorsed by, or sponsored by Devsisters Corporation or the official Cookie Run games. All Cookie Run names, characters, artwork, trademarks, and related intellectual property belong to their respective owners.

All celebration content, award categories, timelines, and fan creations in this project are community-made and unofficial. Nothing here represents an official announcement or product from the developers.

Made with 🍪 by Cookie Runners, for Cookie Runners.

**One Community. Many Adventures. An Everlasting Legacy.**

