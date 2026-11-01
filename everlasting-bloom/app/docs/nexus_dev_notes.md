# Cookie Runners Nexus — Development Notes

Built as Phase 1–2 inside the existing `everlasting-bloom/` Flask tribute.

## What's Real
- `/nexus` route serves the unified Nexus dashboard (sidebar nav, 3 theme modes with persistence, hero, cards grid, stats, timeline preview, archive previews).
- `/nexus-timeline` route serves an interactive timeline engine pulling verified `Timeline` milestones from SQLite.
- 12 verified starter milestones inserted (dates from the master prompt: April 22, April 29, May 7, June 20, Aug 12, Sep 14, Oct 1, Oct 7, Oct 21, Oct 31, Mar 11 remembrance, Dec 8 salute-night).
- Theme switcher uses `localStorage` with `data-theme` attribute. Modes: bloom (default), kingdom, shadow.
- Design system (`nexus.css`) uses the requested palette: Midnight Navy, Deep Blue, Sky Cyan, Bloom Pink, Dream Violet, Golden Cookie, Soft White.
- PureLily archive and Mogra archive are presented as separate sections (not mixed), with respectful language preserved.
- No secrets exposed. No dangerous auto-commands. All buttons have working routes or planned links.

## Not Yet Implemented (Requires Later Phases)
- Full interactive editing of milestones (add/edit/delete with confirmation) — needs admin route extension.
- Project studio CRUD (Everlasting Bloom, ShadowVerse, OvenBreak Decade, CLI, SSH, OS).
- Awards nomination and voting engine.
- Character collection with search/filter.
- Developer workspace terminal integration (should remain read-only reference, never execute dangerous commands).
- Image upload / media gallery (needs safe file upload validation).
- Responsive mobile layout verification (CSS uses responsive media queries but needs real-device testing).

## Security Notes
- App uses Flask's `secret_key` from environment variable with a safe default.
- Database uses parameterized queries (`?` placeholders). No raw SQL injection paths added.
- `EB_ADMIN_PASSWORD` remains the protected admin path.
- No API keys or tokens appear in source.

## Design System Reference
Color tokens in `:root`: `--nexus-midnight: #0B1226`, `--nexus-deep-blue: #14213B`, `--nexus-sky-cyan: #55C9F5`, `--nexus-bloom-pink: #F58FB9`, `--nexus-dream-violet: #9B8BFA`, `--nexus-gold-cookie: #F5C76E`, `--nexus-soft-white: #F3F6FF`.
