#!/usr/bin/env python3
"""
ANGEL OF DOOM — Hermes Agent Terminal UI
========================================
Celestial fantasy terminal interface for Hermes Agent (Cookie Run: Kingdom
Angel of Doom identity).

Colours are extracted from the official Cookie Run: Kingdom "Angel of Doom"
YouTube reference (video ID iTFYKXee6N0, @CookieRunKingdom) and are the
single source of truth for this identity. Warm celestial gold / amber / cream
/ deep brown earth tones — no purple, blue, or pink.

Unofficial fan project — not affiliated with or endorsed by Devsisters.
"""

from __future__ import annotations

import sys
from typing import List

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Colour palette (measured from Angel of Doom reference frame)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ANSI truecolor helper: \x1b[38;2;R;G;Bm  foreground, \x1b[48;2;R;G;Bm bg
def fg(r: int, g: int, b: int) -> str:
    return f"\x1b[38;2;{r};{g};{b}m"

def bg(r: int, g: int, b: int) -> str:
    return f"\x1b[48;2;{r};{g};{b}m"

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"
ITALIC = "\x1b[3m"
UNDERLINE = "\x1b[4m"
BLINK = "\x1b[5m"
REVERSE = "\x1b[7m"

# Palette (measured RGB)
BG_PRIMARY     = (30, 23, 11)    # #1E170B — deep celestial earth (background)
BG_SECONDARY   = (58, 46, 25)    # #3A2E19 — secondary background
BG_TERTIARY    = (90, 70, 36)    # #5A4624 — tertiary background
SURFACE        = (46, 36, 22)    # #2E2416 — card surface
SURFACE_LIFT   = (68, 54, 34)    # #443622 — raised surface
ACCENT_MAIN    = (249, 188, 4)   # #F9BC04 — main accent (celestial gold)
ACCENT_MAIN_DIM= (212, 160, 23)  # #D4A017 — accent dim
ACCENT_SOFT    = (225, 193, 117) # #E1C175 — soft gold
TEXT_PRIMARY   = (243, 232, 208) # #F3E8D0 — primary text (cream)
TEXT_SECONDARY = (201, 185, 132) # #C9B984 — secondary text
TEXT_MUTED     = (142, 122, 78)  # #8E7A4E — muted text
TEXT_INVERSE   = (71, 55, 39)    # #473727 — inverse text
HIGHLIGHT_GLOW = (253, 247, 138) # #FDF78A — glow / highlight
HIGHLIGHT_BRIGHT = (253, 249, 201) # #FDF9C9 — bright highlight
BORDER_DEFAULT = (225, 193, 117) # #E1C175
BORDER_FOCUS   = (249, 188, 4)   # #F9BC04
BORDER_GLOW    = (253, 247, 138) # #FDF78A

# Status colours
STATUS_ONLINE  = ACCENT_MAIN     # #F9BC04
STATUS_OFFLINE = (110, 84, 56)   # #6E5438
STATUS_WARNING = ACCENT_SOFT     # #E1C175
STATUS_ERROR   = (180, 105, 14)  # #B4690E
STATUS_SUCCESS = TEXT_SECONDARY  # #C9B984

# Convenience ANSI strings
C_RESET   = RESET
C_BOLD    = BOLD
C_DIM     = DIM
C_ITALIC  = ITALIC
C_FG_PRIMARY   = fg(*TEXT_PRIMARY)
C_FG_SECONDARY = fg(*TEXT_SECONDARY)
C_FG_MUTED     = fg(*TEXT_MUTED)
C_FG_ACCENT    = fg(*ACCENT_MAIN)
C_FG_ACCENT_DIM= fg(*ACCENT_MAIN_DIM)
C_FG_SOFT      = fg(*ACCENT_SOFT)
C_FG_GLOW      = fg(*HIGHLIGHT_GLOW)
C_FG_BRIGHT    = fg(*HIGHLIGHT_BRIGHT)
C_BG_PRIMARY   = bg(*BG_PRIMARY)
C_BG_SECONDARY = bg(*BG_SECONDARY)
C_BG_SURFACE   = bg(*SURFACE)
C_BG_LIFT      = bg(*SURFACE_LIFT)
C_FG_ONLINE    = fg(*STATUS_ONLINE)
C_FG_OFFLINE   = fg(*STATUS_OFFLINE)
C_FG_WARNING   = fg(*STATUS_WARNING)
C_FG_ERROR     = fg(*STATUS_ERROR)
C_FG_SUCCESS   = fg(*STATUS_SUCCESS)
C_BORDER       = fg(*BORDER_DEFAULT)
C_BORDER_FOCUS = fg(*BORDER_FOCUS)


def clear() -> str:
    return "\x1b[2J\x1b[H"


def hide_cursor() -> str:
    return "\x1b[?25l"


def show_cursor() -> str:
    return "\x1b[?25h"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Box-drawing helpers (celestial, elegant)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DOUBLE = {
    "hl": "\u2551", "hh": "\u2550",
    "tl": "\u2554", "tr": "\u2557", "bl": "\u255A", "br": "\u255D",
    "vl": "\u2551", "cross": "\u256C",
}
SINGLE = {
    "hl": "\u2502", "hh": "\u2500",
    "tl": "\u250C", "tr": "\u2510", "bl": "\u2514", "br": "\u2518",
    "vl": "\u2502", "cross": "\u253C",
}

CELESTIAL_WINGS = [
    "                      /\\                      ",
    "                     /  \\                     ",
    "                    /    \\                    ",
    "                   /      \\                   ",
    "                  /   .  .   \\                  ",
    "                 /   /      \\   \\                 ",
    "                /   /        \\   \\                ",
    "               /   /          \\   \\               ",
    "              /   /            \\   \\              ",
    "             /   /   '    '     \\   \\             ",
    "            /   /   (  o  o  )   \\   \\            ",
    "           /   /    \\  ___  /    \\   \\           ",
    "          /   /     /  \\ /  \\     \\   \\          ",
    "         /   /     /   V   V     \\   \\         ",
    "        /   /      /             \\      \\        ",
    "       /   /      /    '  '  '    \\      \\       ",
    "      /   /      /   /|   |\\   \\   \\      \\      ",
    "     /   /      /   / |   | \\   \\   \\      \\     ",
    "    /   /      /   /  |   |  \\   \\   \\      \\    ",
    "   /   /      /   /   |   |   \\   \\   \\      \\   ",
    "  /   /      /   /    |   |    \\   \\   \\      \\  ",
    " /   /      /   /     |   |     \\   \\   \\      \\ ",
]

HALO = [
    "          .---.          ",
    "        .'     '.        ",
    "       /         \\       ",
    "      ;           ;      ",
    "      |           |      ",
    "      ;           ;      ",
    "       \\         /       ",
    "        '.     .'        ",
    "          '---'          ",
]


def divider(char: str = "\u2550", colour: str = C_FG_SOFT, width: int = 62) -> str:
    return colour + (char * width) + C_RESET


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Status indicators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def status_dot(status: str = "online") -> str:
    """Return a coloured status dot + label."""
    dots = {
        "online":   (C_FG_ONLINE,   "\u25CF  ONLINE"),
        "offline":  (C_FG_OFFLINE,  "\u25CF  OFFLINE"),
        "warning":  (C_FG_WARNING,  "\u25CF  WARNING"),
        "error":    (C_FG_ERROR,    "\u25CF  ERROR"),
        "success":  (C_FG_SUCCESS,  "\u25CF  SUCCESS"),
    }
    colour, label = dots.get(status, dots["online"])
    return colour + label + C_RESET


def status_indicator(key: str, value: str, status: str = "online") -> str:
    return f"{C_FG_SECONDARY}{key}{C_RESET} {C_DIM}{value}{C_RESET}   {status_dot(status)}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Progress bar
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def progress_bar(percent: float, width: int = 26, label: str = "") -> str:
    """A themed progress bar with gold fill on dark track."""
    percent = max(0.0, min(100.0, percent))
    filled = int(width * percent / 100.0)
    empty = width - filled
    track = C_DIM + C_BG_SECONDARY + (" " * empty) + C_RESET
    fill = C_FG_ACCENT + C_BG_ACCENT if False else C_FG_ACCENT
    bar = fill + ("\u2588" * filled) + C_RESET
    pct = f" {C_FG_ACCENT}{percent:5.1f}%{C_RESET}"
    lab = f"{C_FG_SECONDARY}{label}{C_RESET}" if label else ""
    return lab + " " + bar + track + pct


# Terminal doesn't have a bg fill easily; use block chars instead for fill
def progress_bar2(percent: float, width: int = 26, label: str = "") -> str:
    percent = max(0.0, min(100.0, percent))
    filled = int(width * percent / 100.0)
    empty = width - filled
    track = C_DIM + "\u2591" * empty + C_RESET
    fill = C_FG_ACCENT + "\u2588" * filled + C_RESET
    pct = f" {C_FG_ACCENT}{percent:5.1f}%{C_RESET}"
    lab = f"{C_FG_SECONDARY}{label}{C_RESET}" if label else ""
    return lab + " " + fill + track + pct


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Message templates
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def success(message: str) -> str:
    return f"{C_FG_SUCCESS}\u2713  {message}{C_RESET}"


def error(message: str) -> str:
    return f"{C_FG_ERROR}\u2717  {message}{C_RESET}"


def warning(message: str) -> str:
    return f"{C_FG_WARNING}\u26A0  {message}{C_RESET}"


def info(message: str) -> str:
    return f"{C_FG_SECONDARY}\u2139  {message}{C_RESET}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Welcome screen
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WELCOME_TITLE = """\
  ____          _           _               _   _
 / ___|   _ __ | | ___  ___| |_   _  __ _  | \\ | |
 \\___ \\  | '_ \\| |/ _ \\/ __| __| | | |/ _` | |  \\| |
  ___) | | |_) | |  __/ (__| |_  | |_| | (_| | | |\\  |
 |____/  | .__/|_|\\___|\\___|\\__|  \\__,_|\\__,_| |_| \\_|
         |_|
"""

WELCOME_SUB = (
    "Beyond the heavens, beyond destiny, a new era begins."
)

WELCOME_STATS = [
    ("Profile",        "ANGEL OF DOOM",      "online"),
    ("Universe",       "COOKIE RUN",         "online"),
    ("Mode",           "CELESTIAL INTELLIGENCE", "online"),
    ("Identity",       "Celestial Fantasy Intelligence", "online"),
    ("Role",           "Personal AI agent & Cookie Runner project assistant", "online"),
]


def render_welcome() -> str:
    lines: List[str] = []
    lines.append(clear())
    lines.append(C_BG_PRIMARY)
    lines.append(C_FG_PRIMARY)
    # Top celestial border
    lines.append(divider("\u2550", C_FG_GLOW, 70))
    lines.append("")
    # Halo + wings ASCII (celestial decoration)
    for line in HALO:
        lines.append(C_FG_GLOW + " " * 10 + line + C_RESET)
    lines.append("")
    for line in CELESTIAL_WINGS:
        lines.append(C_FG_ACCENT_DIM + line + C_RESET)
    lines.append("")
    # Title
    lines.append(C_BOLD + C_FG_ACCENT + "🪽  ANGEL OF DOOM — HERMES AGENT" + C_RESET)
    lines.append("")
    lines.append(C_ITALIC + C_FG_GLOW + WELCOME_SUB + C_RESET)
    lines.append("")
    lines.append(divider("\u2550", C_FG_SOFT, 70))
    lines.append("")
    # Status block
    for key, value, status in WELCOME_STATS:
        lines.append("  " + status_indicator(key, value, status))
    lines.append("")
    lines.append(divider("\u2550", C_FG_SOFT, 70))
    lines.append("")
    # Quick status indicators
    lines.append("  " + status_indicator("System", "ONLINE", "online"))
    lines.append("  " + status_indicator(" Hermes Agent", "ACTIVE", "online"))
    lines.append("  " + status_indicator(" Cookie Run Knowledge", "LOADED", "online"))
    lines.append("  " + status_indicator(" Termux / Android 14", "READY", "online"))
    lines.append("")
    lines.append(divider("\u2550", C_FG_GLOW, 70))
    lines.append("")
    lines.append(C_DIM + C_FG_MUTED + "Unofficial fan project — not affiliated with or endorsed by Devsisters Corporation." + C_RESET)
    lines.append("")
    lines.append(C_RESET)
    return "".join(lines)


def main() -> None:
    sys.stdout.write(render_welcome())
    sys.stdout.flush()


if __name__ == "__main__":
    main()
