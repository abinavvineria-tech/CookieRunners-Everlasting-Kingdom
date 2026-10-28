#!/usr/bin/env python3
"""CookieVerse Chronicles — Worlds, Legends & My Journey.

Unofficial fan-made digital museum and interactive timeline for Cookie Run
franchise history and personal Cookie Runner journey. Not affiliated with or
endorsed by Devsisters.

Features:
- Franchise history timeline (verified / labeled uncertain)
- Personal journey (from 2026-04-22 KDH start)
- Legendary milestones (achievements, cookies, fan projects)
- Memory museum sections (favorite cookies, reflections)
- Interactive filters (year, game, category)
- Search
- Add / edit events (persisted in SQLite)
- Dark cinematic mode toggle
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, g, jsonify, abort

app = Flask(__name__, instance_relative_config=True)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
app.config["DATABASE"] = os.path.join(app.instance_path, "chronicles.db")

# ------------------------------------------------------------------
# Database helpers
# ------------------------------------------------------------------


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    os.makedirs(app.instance_path, exist_ok=True)
    db = get_db()
    with app.open_resource("schema.sql", mode="r") as f:
        db.executescript(f.read())
    db.commit()


# ------------------------------------------------------------------
# CSRF helpers
# ------------------------------------------------------------------

def generate_csrf_token():
    return "chronicles-csrf-token"


@app.before_request
def csrf_protect():
    if request.method == "POST" or request.method == "PUT" or request.method == "DELETE":
        token = request.headers.get("X-CSRFToken") or request.form.get("csrf_token")
        if not token or token != generate_csrf_token():
            abort(403)


@app.context_processor
def inject_globals():
    return {
        "site_name": "CookieVerse Chronicles",
        "tagline": "Every Cookie Has a Story. Every Runner Leaves a Legacy.",
        "csrf_token": generate_csrf_token,
        "unofficial_label": True,
    }


# ------------------------------------------------------------------
# Schema init (embedded so no external file dependency for simple deploy)
# ------------------------------------------------------------------
SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,         -- ISO YYYY-MM-DD
    category TEXT NOT NULL,     -- franchise | personal | milestone | project | future
    source TEXT NOT NULL DEFAULT 'official', -- official | personal | fan | uncertain
    event_type TEXT NOT NULL DEFAULT 'release', -- release | update | milestone | memory | anniversary | collaboration
    description TEXT,
    is_verified INTEGER DEFAULT 1,
    is_future INTEGER DEFAULT 0,
    details_json TEXT DEFAULT '{}',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_events_date ON events(date);
CREATE INDEX IF NOT EXISTS idx_events_category ON events(category);
CREATE INDEX IF NOT EXISTS idx_events_source ON events(source);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
"""


def init_schema():
    db = get_db()
    db.executescript(SCHEMA)
    db.commit()
    seed_if_empty()


def seed_if_empty():
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    if count > 0:
        return
    defaults = [
        # Franchise history (verified / labeled uncertain)
        ("Cookie Run (original mobile)", "2009-06-12", "franchise", "official", "release",
         "First Cookie Run game released. Date from user-provided fan reference (unofficial anniversary marker). Verify via official archives before quoting as official release date.", 0, 0, '{"label":"user-provided fan date — verify"}'),
        ("Cookie Run: OvenBreak release", "2016-10-27", "franchise", "official", "release",
         "Cookie Run: OvenBreak released. Anniversary observed 2026-10-27.", 1, 0, '{}'),
        ("Cookie Run: Kingdom — launch", "2021-01-21", "franchise", "official", "release",
         "Cookie Run: Kingdom global launch. Verified via public release records.", 1, 0, '{}'),
        ("Cookie Run: Kingdom — 1st Anniversary", "2022-01-21", "franchise", "official", "anniversary",
         "First anniversary of Cookie Run: Kingdom.", 1, 0, '{}'),
        ("Cookie Run: Kingdom — Ancient Heroes update", "2022-05-10", "franchise", "official", "update",
         "Major update introducing Ancient Heroes storyline elements.", 1, 0, '{"label":"approximate — verify exact patch"}'),
        ("Cookie Run: Kingdom — KDH collab (K-pop Demon Hunters x CRK)", "2026-04-22", "franchise", "official", "collaboration",
         "Collaboration event observed by user on personal start date.", 1, 0, '{"label":"collab referenced; verify official naming"}'),
        # Personal journey
        ("My Cookie Run: Kingdom journey begins", "2026-04-22", "personal", "personal", "milestone",
         "Started playing Cookie Run: Kingdom after discovering the K-pop Demon Hunters collaboration. From Tamil Nadu — part of Tamil Nadu Cookie Runners community.", 1, 0, '{}'),
        ("188 days as Cookie Runner (as of 2026-10-27)", "2026-10-27", "personal", "personal", "milestone",
         "Personal play milestone: 188 days active as of OvenBreak anniversary.", 1, 0, '{"label":"personal milestone — not official game event"}'),
        # Legendary milestones (personal achievements)
        ("Eternal Sugar Cookie achievement", "2026-06-15", "milestone", "personal", "milestone",
         "Achieved Eternal Sugar Cookie — a major personal milestone.", 1, 0, '{"label":"personal achievement — not official event"}'),
        ("Timekeeper Cookie unlocked / milestone", "2026-07-04", "milestone", "personal", "milestone",
         "Timekeeper Cookie achievement / milestone reached.", 1, 0, '{"label":"personal milestone"}'),
        ("Awakened White Lily memory", "2026-07-18", "milestone", "personal", "milestone",
         "White Lily and Awakened White Lily remembrance milestone. Dedicated tribute created in fan workspace.", 1, 0, '{"label":"fan tribute milestone"}'),
        ("B!TES Fan Contest victory", "2026-08-01", "milestone", "personal", "milestone",
         "Victory / recognition in B!TES fan contest.", 1, 0, '{"label":"fan contest — personal milestone"}'),
        ("Collector title earned", "2026-09-05", "milestone", "personal", "milestone",
         "Collector title milestone achieved in-game.", 1, 0, '{"label":"personal milestone"}'),
        ("Rajapendra Cookie achievement", "2026-09-22", "milestone", "personal", "milestone",
         "Rajapendra Cookie achievement / milestone.", 1, 0, '{"label":"personal milestone"}'),
        # Projects
        ("CookieVerse: Everlasting Celebrations studio", "2026-10-24", "project", "fan", "release",
         "Fan studio launch — interactive anniversary-based platform with celebration features.", 1, 0, '{}'),
        ("Cookie Run: OvenBreak Anniversary project", "2026-10-27", "project", "fan", "anniversary",
         "Anniversary tribute project for OvenBreak (2016-10-27). Unofficial fan project.", 1, 0, '{"label":"fan anniversary — not official Devsisters event"}'),
        ("ShadowVerse creative work", "2026-10-20", "project", "fan", "release",
         "Creative work / project archive entry for ShadowVerse-inspired content.", 1, 0, '{"label":"fan creative work"}'),
        ("CookieVerse Chronicles launch", "2026-10-28", "project", "fan", "release",
         "This archive — Worlds, Legends & My Journey — launched as a living digital museum.", 1, 0, '{"label":"fan project launch"}'),
        # Memory museum highlights (personal reflections / favorites)
        ("Favorite Cookie: White Lily (Ancient Hero)", "2026-01-01", "personal", "personal", "memory",
         "Personal favorite — White Lily Cookie, Ancient Hero. Dedicated tribute file in workspace.", 0, 0, '{"label":"personal favorite — not an event"}'),
        ("Favorite: Mogra Cookie", "2026-03-15", "personal", "personal", "memory",
         "Mogra Cookie — another favorite reflected in fan work and personal notes.", 0, 0, '{"label":"personal favorite"}'),
        # Future event placeholder (editable by user)
        ("Future milestone: next anniversary / achievement", "2027-01-01", "future", "personal", "milestone",
         "Placeholder for a future milestone. Edit this entry to keep the archive current.", 0, 1, '{"label":"editable future milestone placeholder"}'),
    ]
    db.executemany(
        "INSERT INTO events (title, date, category, source, event_type, description, is_verified, is_future, details_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        defaults,
    )
    db.commit()


# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------

@app.route("/")
def index():
    init_schema()
    db = get_db()
    events = db.execute(
        "SELECT * FROM events ORDER BY date DESC LIMIT 12"
    ).fetchall()
    stats = {
        "total": db.execute("SELECT COUNT(*) FROM events").fetchone()[0],
        "verified": db.execute("SELECT COUNT(*) FROM events WHERE is_verified=1").fetchone()[0],
        "personal": db.execute("SELECT COUNT(*) FROM events WHERE category='personal'").fetchone()[0],
        "milestones": db.execute("SELECT COUNT(*) FROM events WHERE category='milestone'").fetchone()[0],
        "projects": db.execute("SELECT COUNT(*) FROM events WHERE category='project'").fetchone()[0],
    }
    return render_template("index.html", events=events, stats=stats)


@app.route("/timeline")
def timeline():
    init_schema()
    db = get_db()
    events = db.execute(
        "SELECT * FROM events ORDER BY date ASC"
    ).fetchall()
    categories = db.execute("SELECT DISTINCT category FROM events").fetchall()
    years = db.execute("SELECT DISTINCT substr(date,1,4) AS y FROM events ORDER BY y ASC").fetchall()
    return render_template(
        "timeline.html",
        events=events,
        categories=categories,
        years=years,
    )


@app.route("/timeline/filter")
def timeline_filter():
    init_schema()
    db = get_db()
    cat = request.args.get("category", "")
    year = request.args.get("year", "")
    source = request.args.get("source", "")
    q = request.args.get("q", "").strip().lower()
    query = "SELECT * FROM events WHERE 1=1"
    params = []
    if cat:
        query += " AND category = ?"
        params.append(cat)
    if year:
        query += " AND substr(date,1,4) = ?"
        params.append(year)
    if source:
        query += " AND source = ?"
        params.append(source)
    if q:
        query += " AND (LOWER(title) LIKE ? OR LOWER(description) LIKE ?)"
        params.extend((f"%{q}%", f"%{q}%"))
    query += " ORDER BY date ASC"
    events = db.execute(query, params).fetchall()
    return render_template("timeline.html", events=events, categories=db.execute("SELECT DISTINCT category FROM events").fetchall(), years=db.execute("SELECT DISTINCT substr(date,1,4) AS y FROM events ORDER BY y ASC").fetchall())


@app.route("/memory-museum")
def memory_museum():
    init_schema()
    db = get_db()
    favorites = db.execute("SELECT * FROM events WHERE category='personal' OR event_type='memory' ORDER BY date ASC").fetchall()
    milestones = db.execute("SELECT * FROM events WHERE category='milestone' ORDER BY date ASC").fetchall()
    reflections = [
        {"title": "White Lily Tribute", "date": "2026-10-24", "note": "Dedicated tribute to White Lily Cookie — Ancient Hero, truth, sacrifice, courage, friendship, hope. Unofficial fan tribute. Never invented dialogue; only verified quotes: 'I know what must be done.' / 'I will never forgive what I've done.'"},
        {"title": "Journey Reflection", "date": "2026-10-28", "note": "Every Cookie has a story. Every runner leaves a legacy. This archive preserves both official franchise history and my own journey — separated clearly, never mixed."},
    ]
    return render_template("memory_museum.html", favorites=favorites, milestones=milestones, reflections=reflections)


@app.route("/project/<id>")
def project(id):
    init_schema()
    db = get_db()
    evt = db.execute("SELECT * FROM events WHERE id = ?", (id,)).fetchone()
    if evt is None:
        abort(404)
    return render_template("event_detail.html", event=evt)


@app.route("/add", methods=["GET", "POST"])
def add_event():
    init_schema()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        date = request.form.get("date", "").strip()
        category = request.form.get("category", "personal").strip()
        source = request.form.get("source", "personal").strip()
        event_type = request.form.get("event_type", "milestone").strip()
        description = request.form.get("description", "").strip()
        is_verified = 1 if request.form.get("is_verified") else 0
        is_future = 1 if request.form.get("is_future") else 0
        details_json = request.form.get("details_json", "{}").strip()
        if not title or not date:
            return render_template("add.html", error="Title and date are required."), 400
        try:
            datetime.fromisoformat(date)
        except ValueError:
            return render_template("add.html", error="Invalid date format (use YYYY-MM-DD)."), 400
        db = get_db()
        db.execute(
            "INSERT INTO events (title, date, category, source, event_type, description, is_verified, is_future, details_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (title, date, category, source, event_type, description, is_verified, is_future, details_json or "{}"),
        )
        db.commit()
        return redirect(url_for("timeline"))
    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_event(id):
    init_schema()
    db = get_db()
    evt = db.execute("SELECT * FROM events WHERE id = ?", (id,)).fetchone()
    if evt is None:
        abort(404)
    if request.method == "POST":
        title = request.form.get("title", evt["title"]).strip()
        date = request.form.get("date", evt["date"]).strip()
        category = request.form.get("category", evt["category"]).strip()
        source = request.form.get("source", evt["source"]).strip()
        event_type = request.form.get("event_type", evt["event_type"]).strip()
        description = request.form.get("description", evt["description"]).strip()
        is_verified = 1 if request.form.get("is_verified") else 0
        is_future = 1 if request.form.get("is_future") else 0
        details_json = request.form.get("details_json", evt["details_json"]).strip()
        db.execute(
            "UPDATE events SET title=?, date=?, category=?, source=?, event_type=?, description=?, is_verified=?, is_future=?, details_json=? WHERE id=?",
            (title, date, category, source, event_type, description, is_verified, is_future, details_json or "{}", id),
        )
        db.commit()
        return redirect(url_for("timeline"))
    return render_template("edit.html", event=evt)


@app.route("/delete/<int:id>", methods=["POST"])
def delete_event(id):
    init_schema()
    db = get_db()
    db.execute("DELETE FROM events WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("timeline"))


# ------------------------------------------------------------------
# API endpoints
# ------------------------------------------------------------------

@app.route("/api/events")
def api_events():
    init_schema()
    db = get_db()
    rows = db.execute("SELECT * FROM events ORDER BY date ASC").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/events/<int:id>")
def api_event(id):
    init_schema()
    db = get_db()
    row = db.execute("SELECT * FROM events WHERE id=?", (id,)).fetchone()
    if row is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(row))


@app.route("/api/events", methods=["POST"])
def api_create():
    init_schema()
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or request.form.get("title", "")).strip()
    date = (data.get("date") or request.form.get("date", "")).strip()
    category = (data.get("category") or request.form.get("category", "personal")).strip()
    source = (data.get("source") or request.form.get("source", "personal")).strip()
    event_type = (data.get("event_type") or request.form.get("event_type", "milestone")).strip()
    description = (data.get("description") or request.form.get("description", "")).strip()
    is_verified = 1 if (data.get("is_verified") or request.form.get("is_verified")) else 0
    is_future = 1 if (data.get("is_future") or request.form.get("is_future")) else 0
    details_json = (data.get("details_json") or request.form.get("details_json", "{}")).strip()
    if not title or not date:
        return jsonify({"error": "Title and date required"}), 400
    try:
        datetime.fromisoformat(date)
    except ValueError:
        return jsonify({"error": "Invalid date (YYYY-MM-DD)"}), 400
    db = get_db()
    cur = db.execute(
        "INSERT INTO events (title, date, category, source, event_type, description, is_verified, is_future, details_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (title, date, category, source, event_type, description, is_verified, is_future, details_json or "{}"),
    )
    db.commit()
    return jsonify({"id": cur.lastrowid, "title": title, "date": date}), 201


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

if __name__ == "__main__":
    init_schema()
    # Never debug=True in production
    app.run(host="0.0.0.0", port=5000, debug=False)
