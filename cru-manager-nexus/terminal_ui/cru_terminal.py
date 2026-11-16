#!/usr/bin/env python3
"""
CRU MANAGER — Hermes Agent Terminal UI
======================================
Military dark terminal interface for Hermes Agent (Cookie Run Football — Cookie
Runners United identity).

Palette inspired by Shadow Milk Cookie, Head Coach of Cookie Runners United
(Master of Deceit): dark military charcoal/slate with steel and crimson accents.

Unofficial fan project — not affiliated with or endorsed by Devsisters Corporation.
"""

from __future__ import annotations

import sys
from typing import List

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Colour palette (CRU Manager — military dark / steel / crimson)
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

# Palette (measured-style RGB — CRU Manager military theme)
BG_PRIMARY     = (26, 26, 30)    # #1A1A1E — dark military charcoal (background)
BG_SECONDARY   = (42, 42, 54)    # #2A2A36 — secondary background
BG_TERTIARY    = (58, 58, 70)    # #3A3A46 — tertiary background
SURFACE        = (36, 36, 46)    # #24242E — card surface
SURFACE_LIFT   = (58, 58, 70)    # #3A3A46 — raised surface
ACCENT_MAIN    = (192, 197, 206) # #C0C5CE — main accent (steel)
ACCENT_MAIN_DIM= (142, 147, 160) # #8E93A0 — accent dim
ACCENT_SOFT    = (216, 222, 233) # #D8DEE9 — soft steel
ACCENT_CRIMSON = (176, 64, 64)   # #B04040 — crimson (Master of Deceit flair)
ACCENT_CRIMSON_DIM = (142, 52, 52) # #8E3434
ACCENT_CRIMSON_SOFT= (212, 132, 132) # #D48484
TEXT_PRIMARY   = (236, 239, 244) # #ECEFF4 — primary text (steel white)
TEXT_SECONDARY = (190, 200, 214) # #BEC8D6 — secondary text
TEXT_MUTED     = (110, 115, 131) # #6E7383 — muted text
TEXT_INVERSE   = (26, 26, 30)    # #1A1A1E — inverse text
HIGHLIGHT_GLOW = (236, 239, 244) # #ECEFF4 — glow / highlight
HIGHLIGHT_BRIGHT = (255, 255, 255) # #FFFFFF — bright highlight
BORDER_DEFAULT = (216, 222, 233) # #D8DEE9
BORDER_FOCUS   = (192, 197, 206) # #C0C5CE
BORDER_GLOW    = (236, 239, 244) # #ECEFF4

# Status colours
STATUS_ONLINE  = ACCENT_MAIN     # #C0C5CE
STATUS_OFFLINE = (110, 115, 131) # #6E7383
STATUS_WARNING = ACCENT_SOFT     # #D8DEE9
STATUS_ERROR   = ACCENT_CRIMSON  # #B04040
STATUS_SUCCESS = (163, 190, 140) # #A3BE8C

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
C_FG_CRIMSON   = fg(*ACCENT_CRIMSON)
C_FG_CRIMSON_DIM = fg(*ACCENT_CRIMSON_DIM)
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Box-drawing helpers (military, tactical)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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

SHIELD = [
    "                     ___                      ",
    "                    /   \\                     ",
    "                   /  ___  \\                   ",
    "                  /  /   \\  \\                  ",
    "                 /  /     \\  \\                 ",
    "                /  /   __   \\  \\                ",
    "               /  /   /  \\   \\  \\               ",
    "              /  /   /    \\   \\  \\              ",
    "             /  /   /      \\   \\  \\             ",
    "            /  /   /        \\   \\  \\            ",
    "           /  /   /  '  '  \\   \\  \\           ",
    "          /  /   /   (o  o)  \\   \\  \\          ",
    "         /  /   /     \\___/     \\   \\  \\         ",
    "        /  /   /               \\   \\  \\        ",
    "       /  /   /    '     '     \\   \\  \\       ",
    "      /  /   /   /|         |\\   \\   \\  \\      ",
    "     /  /   /   / |         | \\   \\   \\  \\     ",
    "    /  /   /   /  |         |  \\   \\   \\  \\    ",
    "   /  /   /   /   |         |   \\   \\   \\  \\   ",
    "  /  /   /   /    |         |    \\   \\   \\  \\  ",
    " /  /   /   /     |         |     \\   \\   \\  \\ ",
]

TACTICAL_BOARD = [
    "   ╔════════════════════════════════════════╗   ",
    "   ║    TACTICAL BOARD — CRU FORMATION      ║   ",
    "   ║                                        ║   ",
    "   ║      GK                                ║   ",
    "   ║   LB      CB      CB      RB           ║   ",
    "   ║                                        ║   ",
    "   ║      CM      CM      CM                ║   ",
    "   ║                                        ║   ",
    "   ║      CAM                             ║   ",
    "   ║   LW      ST      RW                   ║   ",
    "   ║                                        ║   ",
    "   ╚═══════════════════════════════════════╝   ",
]


def divider(char: str = "\u2550", colour: str = C_FG_SOFT, width: int = 62) -> str:
    return colour + (char * width) + C_RESET


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Status indicators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Progress bar
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def progress_bar(percent: float, width: int = 26, label: str = "") -> str:
    """A themed progress bar with steel fill on dark track."""
    percent = max(0.0, min(100.0, percent))
    filled = int(width * percent / 100.0)
    empty = width - filled
    track = C_DIM + "\u2591" * empty + C_RESET
    fill = C_FG_ACCENT + "\u2588" * filled + C_RESET
    pct = f" {C_FG_ACCENT}{percent:5.1f}%{C_RESET}"
    lab = f"{C_FG_SECONDARY}{label}{C_RESET}" if label else ""
    return lab + " " + fill + track + pct


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Message templates
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def success(message: str) -> str:
    return f"{C_FG_SUCCESS}\u2713  {message}{C_RESET}"


def error(message: str) -> str:
    return f"{C_FG_ERROR}\u2717  {message}{C_RESET}"


def warning(message: str) -> str:
    return f"{C_FG_WARNING}\u26A0  {message}{C_RESET}"


def info(message: str) -> str:
    return f"{C_FG_SECONDARY}\u2139  {message}{C_RESET}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Welcome screen
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WELCOME_TITLE = """\
  ____          _           _               _   _
 / ___|   _ __ | | ___  ___| |_   _  __ _  | \\ | |
 \\___ \\\\  | '_ \\\\| |/ _ \\\\/ __| __| | | |/ _` | |  \\| |
  ___) | | |_) | |  __/ (__| |_  | |_| | (_| | | |\\  |
 |____/  | .__/|_|\\___|\\___|\\__|  \\__,_|\\__,_| |_| \\_|
         |_|
"""

WELCOME_SUB = (
    "ONE CLUB. ONE DREAM. ETERNAL GLORY."
)

WELCOME_STATS = [
    ("Profile",        "CRU MANAGER",              "online"),
    ("Club",           "COOKIE RUNNERS UNITED",    "online"),
    ("Abbreviation",   "CRU",                      "online"),
    ("Head Coach",     "SHADOW MILK COOKIE",       "online"),
    ("Club Captain",   "ABINAV",                   "online"),
    ("Identity",       "AI Football Management Assistant", "online"),
    ("Role",           "CRU football operations & squad development", "online"),
]


def render_welcome() -> str:
    lines: List[str] = []
    lines.append(clear())
    lines.append(C_BG_PRIMARY)
    lines.append(C_FG_PRIMARY)
    # Top tactical border
    lines.append(divider("\u2550", C_FG_GLOW, 70))
    lines.append("")
    # Shield + tactical board ASCII (military decoration)
    for line in SHIELD:
        lines.append(C_FG_CRIMSON_DIM + " " * 8 + line + C_RESET)
    lines.append("")
    # Title
    lines.append(C_BOLD + C_FG_ACCENT + "\u2694  CRU MANAGER — HERMES AGENT" + C_RESET)
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
    lines.append("  " + status_indicator(" CRU Records", "LOADED", "online"))
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
