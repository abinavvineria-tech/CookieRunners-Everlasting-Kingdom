import json
import os
from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)

# Timezone used only when displaying a live date/time.
TIMEZONE = "Asia/Kolkata"

# ---------------------------------------------------------------------------
# Ceremony award data
#
# Every award and winner below is fan-selected for this unofficial
# CookieVerse celebration. None of these are official Devsisters awards.
# ---------------------------------------------------------------------------
AWARDS = [
    {
        "id": "legend-of-the-game",
        "title": "Legend of the Game Award",
        "emoji": "\U0001F3C1",
        "color": "#f5d78b",
        "winners": "White Lily Cookie and Mogra Cookie",
        "winners_emoji": "\U0001F33A\u200D\U0001F3FB\u200D\U0001F33D",
        "tribute": (
            "Two timeless legends honoured together. White Lily Cookie\u2019s "
            "courageous journey and Mogra Cookie\u2019s gentle spirit remind us "
            "why the CookieVerse endures."
        ),
        "medal": "\U0001F947",
    },
    {
        "id": "best-update",
        "title": "Best Update Award",
        "emoji": "\U0001F451",
        "color": "#c084fc",
        "winners": "Cookie Run: Kingdom (CRK)",
        "winners_emoji": "\U0001F451",
        "tribute": (
            "For its adventures, unforgettable characters, storytelling, and "
            "the memories built kingdom after kingdom."
        ),
        "medal": "\U0001F451",
    },
    {
        "id": "best-original-game",
        "title": "Best Original Game Award",
        "emoji": "\U0001F370",
        "color": "#a78bfa",
        "winners": "Cookie Run: OvenBreak",
        "winners_emoji": "\U0001F370",
        "tribute": (
            "The original Cookie Run adventure. Celebrating 10 Years of "
            "Cookie Run: OvenBreak, 27 October 2016 \u2013 27 October 2026."
        ),
        "medal": "\U0001F370",
        "anniversary": True,
        "release_date": "27 October 2016",
        "anniversary_date": "27 October 2026",
    },
    {
        "id": "friendship-teamwork",
        "title": "Friendship & Teamwork Award",
        "emoji": "\U0001F46B",
        "color": "#34d399",
        "winners": "All Cookie Runners",
        "winners_emoji": "\U0001F46B",
        "tribute": (
            "To every Cookie Runner everywhere \u2014 the friendships and "
            "teamwork that make every run brighter."
        ),
        "medal": "\U0001F46B",
    },
    {
        "id": "dragon-legend",
        "title": "Dragon Legend Award",
        "emoji": "\U0001F40F",
        "color": "#fb7185",
        "winners": "The legendary Dragon Cookies",
        "winners_emoji": "\U0001F40F",
        "tribute": (
            "Honouring the mighty dragons who soar through Cookie Run legend."
        ),
        "medal": "\U0001F40F",
    },
    {
        "id": "best-villain",
        "title": "Best Villain Award",
        "emoji": "\U0001F479",
        "color": "#f87171",
        "winners": "Shadow Milk Cookie",
        "winners_emoji": "\U0001F479",
        "tribute": (
            "A captivating shadow who proves every great story needs a "
            "legendary villain."
        ),
        "medal": "\U0001F479",
    },
    {
        "id": "eternal-memory",
        "title": "Eternal Memory Award",
        "emoji": "\U0001F54F",
        "color": "#fbbf24",
        "winners": "White Lily Cookie",
        "winners_emoji": "\U0001F54F",
        "tribute": (
            "Remembered always \u2014 for truth, sacrifice, courage, and hope."
        ),
        "medal": "\U0001F54F",
    },
    {
        "id": "flower-legend",
        "title": "Special Flower Legend Award",
        "emoji": "\U0001F33A",
        "color": "#f472b6",
        "winners": "Mogra Cookie",
        "winners_emoji": "\U0001F33A",
        "tribute": (
            "A gentle blossom whose kindness blooms across the CookieVerse."
        ),
        "medal": "\U0001F33A",
    },
    {
        "id": "cookieverse-legacy",
        "title": "CookieVerse Legacy Award",
        "emoji": "\U0001F389",
        "color": "#818cf8",
        "winners": "Every Cookie Run game",
        "winners_emoji": "\U0001F389",
        "tribute": (
            "From OvenBreak to Kingdom and beyond \u2014 every game that "
            "built this beloved universe."
        ),
        "medal": "\U0001F389",
    },
    {
        "id": "lifetime-achievement",
        "title": "Lifetime Achievement Award",
        "emoji": "\U0001F3C6",
        "color": "#a78bfa",
        "winners": "Devsisters and the teams behind Cookie Run",
        "winners_emoji": "\U0001F3C6",
        "tribute": (
            "For the creators, developers, and teams whose work brought the "
            "CookieVerse to life."
        ),
        "medal": "\U0001F3C6",
    },
]

FINALE_MESSAGE = (
    "Every Cookie has a story. Every game leaves a legacy. "
    "Every Cookie Runner belongs."
)

DISCLAIMER = (
    "This is an unofficial, fan-made Cookie Run celebration created by "
    "Cookie Runners for entertainment and community appreciation. It is not "
    "affiliated with, endorsed by, or sponsored by Devsisters. All award "
    "categories and winners presented here are fan-selected. Cookie Run "
    "names and related intellectual property belong to their respective "
    "owners."
)


def _now_kolkata():
    """Return the current local time labelled Asia/Kolkata.

    Flask runs in the server's local tz; we only label it for display so no
    external timezone library is required.
    """
    return datetime.now().strftime("%d %b %Y, %I:%M %p")


@app.get("/")
def ceremony():
    return render_template(
        "ceremony.html",
        awards=AWARDS,
        finale_message=FINALE_MESSAGE,
        disclaimer=DISCLAIMER,
        now=_now_kolkata(),
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False,
    )
