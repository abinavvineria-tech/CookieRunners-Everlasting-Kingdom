# Everlasting Horizon 🍪✨

> **A New Journey. A New World. An Everlasting Dream.**

Everlasting Horizon is an unofficial, fan-made Cookie Run-inspired digital universe celebrating friendship, creativity, adventures, memories, and the future of Cookie Run.

Built as a functional, responsive web application with a premium dashboard experience, mobile-first design, glowing starfield, and persistent storage.

## Project identity

| | |
|---|---|
| **Name** | Everlasting Horizon |
| **Tagline** | A New Journey. A New World. An Everlasting Dream. |
| **Motto** | One Run. One Dream. One United. |
| **Colours** | Royal blue, gold, white, magical purple |

## Features

1. **Home Dashboard** — Cinematic welcome screen with the project identity, featured characters, worlds, timeline highlights, and open adventures.
2. **CookieVerse** — A collection of Cookie Run-inspired worlds and the stories that live within them.
3. **Character Archives** — Character profiles, histories, personalities, and friendships (with memorable moments between friends).
4. **Journey Timeline** — Milestones, memories, and future plans, presented as an interactive timeline.
5. **Adventure Hub** — Stories and quests with rewards and status (open / completed / upcoming).
6. **Community Hall** — A place to celebrate Cookie Runners and their creativity.
7. **Future Horizon** — Upcoming projects and possibilities, with progress bars and target dates.
8. **Admin Dashboard** — Password-protected administration to create, edit, and delete characters, timeline events, and project settings.

## Website authentication

Everlasting Horizon includes website user accounts (separate from the admin area):

- **Sign up** (`/register`) — create a new account with username, email, and password (passwords are hashed; duplicates are rejected).
- **Sign in** (`/login`) — password-verified login with a `next` redirect back to the page you were visiting.
- **Profile** (`/profile`) — signed-in users can view their account; protected so guests are redirected to sign in.
- **Sign out** (`/logout`) — clears the session.

When signed in, the navigation shows Profile and Sign out; when signed out, it shows Sign in and Join. The admin area (`/admin/`) remains a separate, separate password-protected administration account (default `captain` / `everlasting-horizon-admin`).

## Technical stack

- **Python 3.14** + **Flask 3.1.3** (server-side rendering with Jinja2)
- **SQLite** (persistent storage, one file: `everlasting_horizon.db`)
- **Werkzeug** (password hashing for admin accounts)
- Vanilla **HTML/CSS/JavaScript** — no build step, no heavy frameworks, mobile-first
- Canvas starfield background (respects `prefers-reduced-motion`)

## Getting started

```bash
# 1. Enter the project folder
cd everlasting-horizon

# 2. Install dependencies (uv is recommended; pip also works)
uv pip install -r requirements.txt
# or: pip install -r requirements.txt

# 3. Run the application
python app.py

# 4. Open http://127.0.0.1:5000 in your browser
```

The database is initialised and seeded automatically on first run with friendly demo content. All 8 features are functional with real data — there are no placeholder buttons that do nothing.

### Admin area

The administration dashboard is at `/admin/` and is password-protected.

- Default username: `captain`
- Default password: `everlasting-horizon-admin`

> **Important:** Change the default password before any public use by setting the `EH_ADMIN_PASSWORD` environment variable, or update it in the Admin Dashboard > Settings. The `SECRET_KEY` should also be changed via `EH_SECRET_KEY` in production.

## Admin capabilities

Signed-in administrators can:

- Create, edit, and delete character profiles (including featured flag, colour, emoji)
- Create, edit, and delete timeline events (milestone / memory / future)
- Update project settings (site name, tagline, motto, about text, brand colours)
- Sign in / sign out with session-based authentication

All destructive actions require confirmation.

## Project structure

```
everlasting-horizon/
├── app.py                 # Flask application + all routes
├── database.py            # SQLite connection, schema init, seed data
├── schema.sql             # Database schema
├── requirements.txt       # Python dependencies
├── everlasting_horizon.db # Seeded SQLite database (created on first run)
├── static/
│   ├── css/
│   │   ├── base.css       # Design tokens, reset, layout, components
│   │   ├── components.css # Reusable UI components (cards, timeline, forms)
│   │   └── particles.css  # Starfield canvas styles
│   └── js/
│       ├── app.js         # Mobile nav, flash dismiss, interactions
│       └── particles.js   # Animated starfield background
└── templates/
    ├── base.html          # Shared layout (nav, banner, footer)
    ├── home.html          # Home dashboard
    ├── cookieverse.html   # Worlds & stories
    ├── characters.html    # Character archive list
    ├── character_detail.html
    ├── timeline.html
    ├── adventures.html
    ├── adventure_detail.html
    ├── community.html
    ├── future.html
    ├── about.html
    ├── errors/404.html
    ├── errors/500.html
    └── admin/
        ├── login.html
        ├── dashboard.html
        ├── characters.html
        ├── character_form.html
        ├── timeline.html
        ├── timeline_form.html
        └── settings.html
```

## Unofficial fan-project disclaimer

**Everlasting Horizon is an unofficial, community-made fan project.**

It is **not** affiliated with, endorsed by, or sponsored by Devsisters Corporation or the official Cookie Run games. All Cookie Run names, characters, artwork, trademarks, and related intellectual property belong to their respective owners.

All content in this project is original fan-created material made for celebration, creativity, and community fun. No characters, stories, or events presented here are official announcements or products. No commercial use is implied or permitted.

Made with 🍪 by Cookie Runners, for Cookie Runners.

**One Run. One Dream. One United.**
