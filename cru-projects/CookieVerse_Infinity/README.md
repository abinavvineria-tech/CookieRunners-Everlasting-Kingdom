# CookieVerse Infinity

CookieVerse Infinity is an independent, unofficial, fan-made Cookie Run-inspired fantasy universe founded by Captain Abinav in 2026.

## Phase 1: CookieVerse Central

This first milestone is a responsive Vite + React landing page and central dashboard with:

- Five-division navigation
- Captain Abinav welcome experience
- Project status, roadmap and announcement panels
- Responsive mobile layout
- Interactive navigation feedback without pretending future integrations are live
- Accessible buttons, labels and descriptive metadata

## Local setup

Requirements: Node.js 20+ and npm.

```sh
npm install
npm run dev
```

Open the local URL printed by Vite. Build a production bundle with `npm run build`, then preview it with `npm run preview`.

## Architecture

- `index.html` — app shell and metadata
- `src/main.jsx` — CookieVerse Central UI and local interaction state
- `src/styles.css` — visual system, responsive layout and fantasy styling
- `vite.config.js` — Vite React configuration

The page is intentionally frontend-only in Phase 1. Hermes, Telegram, AI APIs, PostgreSQL, authentication and community accounts are not connected yet; those require explicit backend design, credentials and external configuration in later phases. No secrets belong in this repository.

## Creative and IP notice

CookieVerse Infinity is an unofficial fan-made initiative. Use original artwork, original characters and original lore for future content. Cookie Run is the property of its respective rights holders.

ONE RUN. ONE DREAM. ONE UNITED. 🌸
