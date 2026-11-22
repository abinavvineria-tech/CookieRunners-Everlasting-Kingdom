import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.environ.get(
    "CRU_DATABASE_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookie_runners_hq.db"),
)

GAME_STATUSES = [
    "Officially announced",
    "In development",
    "Release date announced",
    "Released",
    "Unconfirmed / Rumoured",
]

CONFIRMATION_STATUSES = ["confirmed", "rumour", "speculation"]

ANNOUNCEMENT_TYPES = ["news", "update", "maintenance", "event", "release", "anniversary"]

CALENDAR_ITEM_TYPES = [
    "launch",
    "update",
    "maintenance",
    "event",
    "anniversary",
    "announcement",
]


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            description TEXT,
            color TEXT DEFAULT '#8b5cf6',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            description TEXT,
            short_description TEXT,
            release_date TEXT,
            platforms TEXT,
            developer TEXT DEFAULT 'Devsisters',
            publisher TEXT DEFAULT 'Devsisters',
            official_website TEXT,
            announcement_link TEXT,
            trailer_url TEXT,
            status TEXT DEFAULT 'Released',
            game_type TEXT DEFAULT 'other',
            featured INTEGER DEFAULT 0,
            image_url TEXT,
            confirmation_status TEXT DEFAULT 'confirmed',
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            summary TEXT,
            content TEXT,
            category_id INTEGER,
            announcement_type TEXT DEFAULT 'news',
            confirmation_status TEXT DEFAULT 'confirmed',
            source_url TEXT,
            source_name TEXT,
            published_at TEXT,
            is_pinned INTEGER DEFAULT 0,
            is_published INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS game_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            title TEXT NOT NULL,
            version TEXT,
            patch_notes TEXT,
            release_date TEXT,
            maintenance INTEGER DEFAULT 0,
            source_url TEXT,
            confirmation_status TEXT DEFAULT 'confirmed',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES games(id)
        )"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            start_date TEXT,
            end_date TEXT,
            event_type TEXT DEFAULT 'event',
            image_url TEXT,
            source_url TEXT,
            confirmation_status TEXT DEFAULT 'confirmed',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES games(id)
        )"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS calendar_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            item_type TEXT,
            start_date TEXT,
            end_date TEXT,
            all_day INTEGER DEFAULT 1,
            game_id INTEGER,
            url TEXT,
            confirmation_status TEXT DEFAULT 'confirmed',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES games(id)
        )"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'admin',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )"""
    )

    conn.commit()
    conn.close()


def seed_data():
    """Seed default categories, games and one admin user. Never overwrites existing rows."""
    conn = get_conn()
    c = conn.cursor()

    categories = [
        ("News", "news", "General Cookie Run news and community stories", "#ef4444"),
        ("Game Updates", "update", "Game updates, patches and new versions", "#3b82f6"),
        ("Maintenance", "maintenance", "Scheduled maintenance and server notices", "#f59e0b"),
        ("Events", "event", "In-game events and campaigns", "#8b5cf6"),
        ("Releases", "release", "New game releases and release dates", "#10b981"),
        ("Anniversaries", "anniversary", "Game anniversaries and celebrations", "#ec4899"),
    ]
    for name, slug, desc, color in categories:
        c.execute(
            "INSERT OR IGNORE INTO categories (name, slug, description, color) VALUES (?, ?, ?, ?)",
            (name, slug, desc, color),
        )

    games = [
        (
            "Cookie Run: Kingdom",
            "cookie-run-kingdom",
            "A kingdom-building RPG where cookies band together to rebuild the Cookie Kingdom. "
            "Collect cookies, build your kingdom, and battle in the Kingdom Arena.",
            "Build your cookie kingdom and battle with your favorite cookies.",
            "2021-01-21",
            "iOS, Android, PC",
            "Devsisters",
            "Devsisters",
            "https://kingdom.cookie-run.com/",
            "https://www.devsisters.com/",
            "https://www.youtube.com/watch?v=9L0c3tVZz5k",
            "Released",
            "kingdom",
            1,
            "",
            "confirmed",
            "Global launch date. Verify current details on the official Kingdom website.",
        ),
        (
            "Cookie Run: OvenBreak",
            "cookie-run-ovenbreak",
            "The endless runner where cookies escape the oven. Run, jump, and slide with "
            "jellies, pets, and game-changing cookie skills.",
            "Endless-runner action with Cookie Run's classic cookies.",
            "2016-12-01",
            "iOS, Android",
            "Devsisters",
            "Devsisters",
            "https://ovenbreak.cookie-run.com/",
            "https://www.devsisters.com/",
            "",
            "Released",
            "ovenbreak",
            1,
            "",
            "confirmed",
            "Global release. Verify current details on the official OvenBreak website.",
        ),
        (
            "Cookie Run: Tower of Adventures",
            "cookie-run-tower-of-adventures",
            "An officially announced upcoming Cookie Run title. Adventure awaits in the tower.",
            "Upcoming Cookie Run adventure game announced by Devsisters.",
            None,
            "To be announced",
            "Devsisters",
            "Devsisters",
            "https://www.devsisters.com/",
            "https://www.devsisters.com/",
            "",
            "Officially announced",
            "upcoming",
            1,
            "",
            "confirmed",
            "Announced by Devsisters. Release date and platforms not yet confirmed.",
        ),
        (
            "Cookie Run: Witch's Castle",
            "cookie-run-witchs-castle",
            "A Cookie Run title whose current status has not been confirmed by Devsisters.",
            "Cookie Run title — status unverified.",
            None,
            "To be announced",
            "Devsisters",
            "Devsisters",
            "https://www.devsisters.com/",
            "https://www.devsisters.com/",
            "",
            "Unconfirmed / Rumoured",
            "other",
            0,
            "",
            "rumour",
            "UNVERIFIED: Not presented as official news. Treat as rumour until Devsisters confirms.",
        ),
    ]
    for (
        title, slug, desc, short, release_date, platforms, developer, publisher,
        website, announcement_link, trailer, status, game_type, featured, image,
        conf, notes,
    ) in games:
        c.execute(
            """INSERT OR IGNORE INTO games
               (title, slug, description, short_description, release_date, platforms,
                developer, publisher, official_website, announcement_link, trailer_url,
                status, game_type, featured, image_url, confirmation_status, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                title, slug, desc, short, release_date, platforms, developer, publisher,
                website, announcement_link, trailer, status, game_type, featured, image,
                conf, notes,
            ),
        )

    announcements = [
        (
            "Welcome to Cookie Runners HQ",
            "welcome-to-cookie-runners-hq",
            "The community hub for tracking Cookie Run announcements, updates and events.",
            "Cookie Runners HQ is now live. Track official Devsisters announcements, game "
            "updates, upcoming releases and in-game events in one place.",
            1,  # News category
            "news",
            "confirmed",
            None,
            "Cookie Runners HQ",
            None,
            1,
            1,
        ),
        (
            "Cookie Run: Kingdom launched globally",
            "cookie-run-kingdom-launched",
            "Cookie Run: Kingdom launched globally on January 21, 2021.",
            "Cookie Run: Kingdom's global launch is a matter of public record.",
            5,  # Releases
            "release",
            "confirmed",
            "https://kingdom.cookie-run.com/",
            "Devsisters",
            "2021-01-21",
            0,
            1,
        ),
        (
            "Cookie Run: Tower of Adventures officially announced",
            "tower-of-adventures-announced",
            "Devsisters announced Cookie Run: Tower of Adventures as an upcoming title.",
            "Upcoming game announced by Devsisters. Release date and platforms TBD.",
            5,
            "release",
            "confirmed",
            "https://www.devsisters.com/",
            "Devsisters",
            None,
            0,
            1,
        ),
        (
            "Rumoured: new Cookie Run title in development",
            "rumoured-new-cookie-run-title",
            "Unconfirmed reports suggest a new Cookie Run title may be in development.",
            "UNVERIFIED rumour. Not official Devsisters news. Do not share as fact.",
            1,
            "news",
            "rumour",
            None,
            "Cookie Runners HQ (editorial)",
            None,
            0,
            1,
        ),
        (
            "Speculation: possible 2026 Cookie Run collaborations",
            "speculated-2026-collaborations",
            "Community speculation about possible Cookie Run collaborations in 2026.",
            "SPECULATION only. Nothing confirmed by Devsisters.",
            1,
            "news",
            "speculation",
            None,
            "Cookie Runners HQ (editorial)",
            None,
            0,
            1,
        ),
    ]
    cat_ids = {row["slug"]: row["id"] for row in c.execute("SELECT id, slug FROM categories").fetchall()}
    for (
        title, slug, summary, content, cat_slug, atype, conf, source_url, source_name,
        published_at, pinned, published,
    ) in announcements:
        cat_id = cat_ids.get(cat_slug)
        c.execute(
            """INSERT OR IGNORE INTO announcements
               (title, slug, summary, content, category_id, announcement_type,
                confirmation_status, source_url, source_name, published_at,
                is_pinned, is_published)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (title, slug, summary, content, cat_id, atype, conf, source_url, source_name,
             published_at, pinned, published),
        )

    # Game updates
    updates = [
        (1, "Cookie Run: Kingdom update notes", "v8.x", "Sample placeholder — replace with real patch notes from Devsisters.", None, 0, "https://kingdom.cookie-run.com/", "confirmed"),
    ]
    for gid, title, version, notes, rel_date, maintenance, source_url, conf in updates:
        c.execute(
            """INSERT OR IGNORE INTO game_updates
               (game_id, title, version, patch_notes, release_date, maintenance,
                source_url, confirmation_status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (gid, title, version, notes, rel_date, maintenance, source_url, conf),
        )

    # Events
    events = [
        (1, "Kingdom Anniversary Celebration", "Annual Cookie Run: Kingdom anniversary event.", None, None, "anniversary", "", "https://kingdom.cookie-run.com/", "rumour"),
    ]
    for gid, title, desc, start, end, etype, image, source_url, conf in events:
        c.execute(
            """INSERT OR IGNORE INTO events
               (game_id, title, description, start_date, end_date, event_type,
                image_url, source_url, confirmation_status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (gid, title, desc, start, end, etype, image, source_url, conf),
        )

    # Calendar items
    calendar_items = [
        ("Cookie Run: Kingdom — Global Launch", "Released January 21, 2021.", "launch", "2021-01-21", None, 1, 1, None, "confirmed"),
        ("Cookie Run: Tower of Adventures — Expected reveal window", "Watch Devsisters channels for an official release-date announcement.", "announcement", None, None, 1, 3, None, "rumour"),
        ("Cookie Run: Kingdom — Anniversary (annual pattern)", "Kingdom typically celebrates its anniversary in late January. Date not confirmed for this year.", "anniversary", None, None, 1, 1, None, "speculation"),
    ]
    for title, desc, itype, start, end, all_day, game_id, url, conf in calendar_items:
        c.execute(
            """INSERT OR IGNORE INTO calendar_items
               (title, description, item_type, start_date, end_date, all_day, game_id, url,
                confirmation_status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (title, desc, itype, start, end, all_day, game_id, url, conf),
        )

    # Default admin user
    admin_user = os.environ.get("ADMIN_USERNAME", "admin")
    admin_password = os.environ.get("ADMIN_PASSWORD", "changeme-admin-123")
    c.execute("SELECT 1 FROM users WHERE username = ?", (admin_user,))
    if not c.fetchone():
        c.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'admin')",
            (admin_user, generate_password_hash(admin_password)),
        )
        print(f"[seed] Created default admin user '{admin_user}'. Change the password in production!")

    conn.commit()
    conn.close()


# --------------------------- Queries ---------------------------

def dict_row(row):
    return dict(row) if row else None


def get_categories():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM categories ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_category(slug):
    conn = get_conn()
    row = conn.execute("SELECT * FROM categories WHERE slug = ?", (slug,)).fetchone()
    conn.close()
    return dict_row(row)


def get_games(featured_only=False, game_type=None, status=None, q=None):
    conn = get_conn()
    query = "SELECT * FROM games WHERE 1=1"
    params = []
    if featured_only:
        query += " AND featured = 1"
    if game_type:
        query += " AND game_type = ?"
        params.append(game_type)
    if status:
        query += " AND status = ?"
        params.append(status)
    if q:
        query += " AND (title LIKE ? OR description LIKE ? OR short_description LIKE ?)"
        like = f"%{q}%"
        params.extend([like, like, like])
    query += " ORDER BY featured DESC, title"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_game(slug):
    conn = get_conn()
    row = conn.execute("SELECT * FROM games WHERE slug = ?", (slug,)).fetchone()
    conn.close()
    return dict_row(row)


def get_game_by_id(gid):
    conn = get_conn()
    row = conn.execute("SELECT * FROM games WHERE id = ?", (gid,)).fetchone()
    conn.close()
    return dict_row(row)


def add_game(data):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """INSERT INTO games
           (title, slug, description, short_description, release_date, platforms,
            developer, publisher, official_website, announcement_link, trailer_url,
            status, game_type, featured, image_url, confirmation_status, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        tuple(data[k] for k in [
            "title", "slug", "description", "short_description", "release_date",
            "platforms", "developer", "publisher", "official_website",
            "announcement_link", "trailer_url", "status", "game_type", "featured",
            "image_url", "confirmation_status", "notes",
        ]),
    )
    gid = c.lastrowid
    conn.commit()
    conn.close()
    return gid


def update_game(gid, data):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """UPDATE games SET title=?, slug=?, description=?, short_description=?,
           release_date=?, platforms=?, developer=?, publisher=?, official_website=?,
           announcement_link=?, trailer_url=?, status=?, game_type=?, featured=?,
           image_url=?, confirmation_status=?, notes=?, updated_at=CURRENT_TIMESTAMP
           WHERE id=?""",
        tuple(data[k] for k in [
            "title", "slug", "description", "short_description", "release_date",
            "platforms", "developer", "publisher", "official_website",
            "announcement_link", "trailer_url", "status", "game_type", "featured",
            "image_url", "confirmation_status", "notes",
        ]) + (gid,),
    )
    conn.commit()
    conn.close()


def delete_game(gid):
    conn = get_conn()
    conn.execute("DELETE FROM games WHERE id = ?", (gid,))
    conn.commit()
    conn.close()


def get_announcements(published_only=True, category=None, atype=None, conf=None, q=None, limit=None):
    conn = get_conn()
    query = """SELECT a.*, c.name AS category_name, c.slug AS category_slug, c.color AS category_color
               FROM announcements a LEFT JOIN categories c ON a.category_id = c.id WHERE 1=1"""
    params = []
    if published_only:
        query += " AND a.is_published = 1"
    if category:
        query += " AND c.slug = ?"
        params.append(category)
    if atype:
        query += " AND a.announcement_type = ?"
        params.append(atype)
    if conf:
        query += " AND a.confirmation_status = ?"
        params.append(conf)
    if q:
        query += " AND (a.title LIKE ? OR a.summary LIKE ? OR a.content LIKE ?)"
        like = f"%{q}%"
        params.extend([like, like, like])
    query += " ORDER BY a.is_pinned DESC, COALESCE(a.published_at, a.created_at) DESC"
    if limit:
        query += " LIMIT ?"
        params.append(limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_announcement(slug):
    conn = get_conn()
    row = conn.execute(
        """SELECT a.*, c.name AS category_name, c.color AS category_color
           FROM announcements a LEFT JOIN categories c ON a.category_id = c.id
           WHERE a.slug = ?""", (slug,)
    ).fetchone()
    conn.close()
    return dict_row(row)


def add_announcement(data):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """INSERT INTO announcements
           (title, slug, summary, content, category_id, announcement_type,
            confirmation_status, source_url, source_name, published_at, is_pinned, is_published)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        tuple(data[k] for k in [
            "title", "slug", "summary", "content", "category_id", "announcement_type",
            "confirmation_status", "source_url", "source_name", "published_at",
            "is_pinned", "is_published",
        ]),
    )
    aid = c.lastrowid
    conn.commit()
    conn.close()
    return aid


def update_announcement(aid, data):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """UPDATE announcements SET title=?, slug=?, summary=?, content=?,
           category_id=?, announcement_type=?, confirmation_status=?, source_url=?,
           source_name=?, published_at=?, is_pinned=?, is_published=?
           WHERE id=?""",
        tuple(data[k] for k in [
            "title", "slug", "summary", "content", "category_id", "announcement_type",
            "confirmation_status", "source_url", "source_name", "published_at",
            "is_pinned", "is_published",
        ]) + (aid,),
    )
    conn.commit()
    conn.close()


def delete_announcement(aid):
    conn = get_conn()
    conn.execute("DELETE FROM announcements WHERE id = ?", (aid,))
    conn.commit()
    conn.close()


def get_updates(game_id=None, maintenance=None, conf=None, limit=None):
    conn = get_conn()
    query = """SELECT u.*, g.title AS game_title FROM game_updates u
               LEFT JOIN games g ON u.game_id = g.id WHERE 1=1"""
    params = []
    if game_id:
        query += " AND u.game_id = ?"
        params.append(game_id)
    if maintenance is not None:
        query += " AND u.maintenance = ?"
        params.append(1 if maintenance else 0)
    if conf:
        query += " AND u.confirmation_status = ?"
        params.append(conf)
    query += " ORDER BY u.release_date DESC, u.created_at DESC"
    if limit:
        query += " LIMIT ?"
        params.append(limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_update(data):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """INSERT INTO game_updates
           (game_id, title, version, patch_notes, release_date, maintenance,
            source_url, confirmation_status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        tuple(data[k] for k in [
            "game_id", "title", "version", "patch_notes", "release_date",
            "maintenance", "source_url", "confirmation_status",
        ]),
    )
    uid = c.lastrowid
    conn.commit()
    conn.close()
    return uid


def delete_update(uid):
    conn = get_conn()
    conn.execute("DELETE FROM game_updates WHERE id = ?", (uid,))
    conn.commit()
    conn.close()


def get_events(game_id=None, conf=None, upcoming_only=False):
    conn = get_conn()
    query = """SELECT e.*, g.title AS game_title FROM events e
               LEFT JOIN games g ON e.game_id = g.id WHERE 1=1"""
    params = []
    if game_id:
        query += " AND e.game_id = ?"
        params.append(game_id)
    if conf:
        query += " AND e.confirmation_status = ?"
        params.append(conf)
    if upcoming_only:
        query += " AND e.end_date >= date('now')"
    query += " ORDER BY e.start_date IS NULL, e.start_date, e.title"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_event(data):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """INSERT INTO events
           (game_id, title, description, start_date, end_date, event_type,
            image_url, source_url, confirmation_status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        tuple(data[k] for k in [
            "game_id", "title", "description", "start_date", "end_date",
            "event_type", "image_url", "source_url", "confirmation_status",
        ]),
    )
    eid = c.lastrowid
    conn.commit()
    conn.close()
    return eid


def delete_event(eid):
    conn = get_conn()
    conn.execute("DELETE FROM events WHERE id = ?", (eid,))
    conn.commit()
    conn.close()


def get_calendar_items(year=None, month=None, view="month"):
    conn = get_conn()
    query = """SELECT c.*, g.title AS game_title FROM calendar_items c
               LEFT JOIN games g ON c.game_id = g.id WHERE 1=1"""
    params = []
    if view == "month" and year and month:
        start = f"{year:04d}-{month:02d}-01"
        if month == 12:
            end = f"{year + 1:04d}-01-01"
        else:
            end = f"{year:04d}-{month + 1:02d}-01"
        query += " AND c.start_date >= ? AND (c.end_date IS NULL OR c.end_date < ?)"
        params.extend([start, end])
    elif view == "week" and year and month:
        # Approximate: return the whole month; JS highlights the week
        start = f"{year:04d}-{month:02d}-01"
        if month == 12:
            end = f"{year + 1:04d}-01-01"
        else:
            end = f"{year:04d}-{month + 1:02d}-01"
        query += " AND c.start_date >= ? AND (c.end_date IS NULL OR c.end_date < ?)"
        params.extend([start, end])
    query += " ORDER BY c.start_date IS NULL, c.start_date, c.title"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_calendar_item(data):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """INSERT INTO calendar_items
           (title, description, item_type, start_date, end_date, all_day,
            game_id, url, confirmation_status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        tuple(data[k] for k in [
            "title", "description", "item_type", "start_date", "end_date",
            "all_day", "game_id", "url", "confirmation_status",
        ]),
    )
    cid = c.lastrowid
    conn.commit()
    conn.close()
    return cid


def delete_calendar_item(cid):
    conn = get_conn()
    conn.execute("DELETE FROM calendar_items WHERE id = ?", (cid,))
    conn.commit()
    conn.close()


def get_dashboard_data():
    conn = get_conn()
    data = {}
    data["latest_announcements"] = [
        dict(r) for r in conn.execute(
            """SELECT a.*, c.name AS category_name, c.color AS category_color
               FROM announcements a LEFT JOIN categories c ON a.category_id = c.id
               WHERE a.is_published = 1
               ORDER BY a.is_pinned DESC, COALESCE(a.published_at, a.created_at) DESC
               LIMIT 6"""
        ).fetchall()
    ]
    data["upcoming_releases"] = [
        dict(r) for r in conn.execute(
            """SELECT * FROM games
               WHERE status IN ('Officially announced', 'In development', 'Release date announced')
               ORDER BY title LIMIT 5"""
        ).fetchall()
    ]
    data["recent_updates"] = [
        dict(r) for r in conn.execute(
            """SELECT u.*, g.title AS game_title FROM game_updates u
               LEFT JOIN games g ON u.game_id = g.id
               ORDER BY u.created_at DESC LIMIT 6"""
        ).fetchall()
    ]
    data["current_events"] = [
        dict(r) for r in conn.execute(
            """SELECT e.*, g.title AS game_title FROM events e
               LEFT JOIN games g ON e.game_id = g.id
               WHERE (e.end_date IS NULL OR e.end_date >= date('now'))
               ORDER BY e.start_date IS NULL, e.start_date LIMIT 6"""
        ).fetchall()
    ]
    data["featured_games"] = [
        dict(r) for r in conn.execute(
            "SELECT * FROM games WHERE featured = 1 ORDER BY title"
        ).fetchall()
    ]
    data["community_news"] = [
        dict(r) for r in conn.execute(
            """SELECT a.*, c.name AS category_name, c.color AS category_color
               FROM announcements a LEFT JOIN categories c ON a.category_id = c.id
               WHERE a.is_published = 1 AND a.announcement_type = 'news'
               ORDER BY COALESCE(a.published_at, a.created_at) DESC LIMIT 5"""
        ).fetchall()
    ]
    conn.close()
    return data


def verify_user(username, password):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if row and check_password_hash(row["password_hash"], password):
        return dict(row)
    return None
