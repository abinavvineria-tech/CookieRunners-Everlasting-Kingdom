# Everbloom Nexus — Hermes Agent Integration

Integration name: everbloomnexus
Project: Champions League Countdown Nexus
Event: Cookie Run Kingdom Champions League Welcome Night
Date: 18 November 2026
Kickoff: 8:30 PM IST (Asia/Kolkata)
Type: Unofficial fan project (not Devsisters)

Purpose:
This is a dedicated Hermes agent profile integration that can:
1. Explain the event countdown status.
2. Report the target event date and timezone.
3. Help maintain the countdown application.
4. Diagnose application errors.
5. Provide a concise event status summary.

Backend endpoints used by the integration:
| Endpoint | Method | Purpose |
| /api/event | GET | Current event config + countdown state (days/hours/minutes/seconds, launched flag). |
| /api/event | POST | Update event configuration (validated: date YYYY-MM-DD, time HH:MM, valid timezone). |
| /api/health | GET | Health check ({"status": "ok"}). |

Example integration responses:
- Countdown status: The Champions League Welcome Night is counting down. Target: 11 November 2026, 8:30 PM IST (Asia/Kolkata). X days, Y hours, Z minutes remaining. Status: counting_down.
- Event started: The Championship has begun! Welcome Night is now live. Status: launched.
- Event date & timezone: Target event: Cookie Run Kingdom Champions League Welcome Night on 11 November 2026 at 20:30 Asia/Kolkata (8:30 PM IST).
- Diagnostics: Backend health: OK. /api/event reachable. Event config loaded from data/events.json. Countdown calculated from configured date/time/timezone — never hardcoded.

Setup for Hermes:
1. Ensure the Champions League Countdown Nexus backend is running (see README "Setup").
2. Point the Hermes everbloomnexus profile at the backend URL (default http://127.0.0.1:5000).
3. The integration reads /api/event to build status summaries and /api/health to diagnose errors.

Notes:
- No existing Hermes profiles or configuration files were overwritten.
- All event data lives in data/events.json; edits persist across restarts when PERSIST_EVENTS=true.
- Unofficial fan project — not affiliated with or endorsed by Devsisters.
