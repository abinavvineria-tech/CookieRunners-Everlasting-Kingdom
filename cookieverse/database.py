import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "cookieverse.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Categories
    c.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        slug TEXT UNIQUE,
        description TEXT
    )''')
    # Winners
    c.execute('''CREATE TABLE IF NOT EXISTS winners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        name TEXT,
        role_text TEXT,
        year INTEGER,
        image_path TEXT,
        description TEXT
    )''')
    # Nominees
    c.execute('''CREATE TABLE IF NOT EXISTS nominees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        name TEXT,
        year INTEGER,
        nominated_by TEXT
    )''')
    # Editions
    c.execute('''CREATE TABLE IF NOT EXISTS editions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        title TEXT,
        tagline TEXT
    )''')
    # Moments
    c.execute('''CREATE TABLE IF NOT EXISTS moments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        year INTEGER
    )''')
    # Admin users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT
    )''')
    conn.commit()
    conn.close()

# All 15 award categories
CATEGORIES = [
    ("Golden Ballon d'Or", "golden-ballon-dor", "The highest honor — the Golden Ball of Cookie Legends."),
    ("Golden Heart Award", "golden-heart", "For compassion, leadership, and a golden heart."),
    ("Golden Teammate Award", "golden-teammate", "Celebrating the ultimate teammate."),
    ("Golden Legend Award", "golden-legend", "For legendary status across all Cookie Run worlds."),
    ("Rising Star Award", "rising-star", "The brightest new legend rising."),
    ("Best Guardian Award", "best-guardian", "For the protector of all cookies."),
    ("Best Villain Award", "best-villain", "The most iconic and unforgettable adversary."),
    ("Best Duo Award", "best-duo", "An unforgettable pair of cookies."),
    ("Best Friendship Award", "best-friendship", "Celebrating bonds that shine forever."),
    ("Golden Leadership Award", "golden-leadership", "Leading with vision, courage, and unity."),
    ("Best Teammate Award", "best-teammate", "The teammate every legend dreams of."),
    ("Eternal Legacy Award", "eternal-legacy", "A legacy that will never fade."),
    ("Golden Memory Award", "golden-memory", "The most unforgettable scene or moment."),
    ("Best Cookie Run Game Award", "best-game", "Celebrating the best Cookie Run experience."),
    ("Best Update Award", "best-update", "The update that changed everything."),
    # Extended categories per spec
    ("Cookie Runners Community Award", "community-award", "Celebrating the heart of the Cookie Runners community."),
    ("Creative Cookie Runner Award", "creative-runner", "For creativity, art, and community contributions."),
    ("Lifetime Achievement Award", "lifetime-achievement", "A lifetime of legendary contribution to Cookie Run."),
]

def seed_first_edition():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Insert categories
    for name, slug, desc in CATEGORIES:
        c.execute("INSERT OR IGNORE INTO categories (name, slug, description) VALUES (?, ?, ?)", (name, slug, desc))
    conn.commit()

    # Seed first edition winners (predefined, never overwritten accidentally)
    # We use a special check: if already present with role_text matching, skip; else add if missing
    winners_2026 = [
        (1, "White Lily Cookie", "Co-winner — Golden Ballon d'Or 2026", 2026, "/static/images/white_lily.jpg", "A gentle soul who carries eternal grace. Co-winner of the first Golden Ballon d'Or."),
        (1, "Mogra Cookie", "Co-winner — Golden Ballon d'Or 2026", 2026, "/static/images/mogra.jpg", "A powerful presence with a golden heart. Co-winner of the first Golden Ballon d'Or."),
        (2, "White Lily Cookie", "Golden Heart Award 2026", 2026, "/static/images/white_lily.jpg", "Compassion that lights the way forever."),
        (2, "Mogra Cookie", "Golden Heart Award 2026", 2026, "/static/images/mogra.jpg", "Strength rooted in kindness and golden heart."),
        (3, "Pure Vanilla Cookie", "Golden Teammate Award 2026", 2026, "/static/images/pure_vanilla.jpg", "The friend every legend needs and the ultimate teammate."),
    ]
    for cat_id, name, role_text, year, image_path, desc in winners_2026:
        c.execute("SELECT 1 FROM winners WHERE category_id = ? AND name = ? AND role_text = ?", (cat_id, name, role_text))
        if not c.fetchone():
            c.execute("INSERT INTO winners (category_id, name, role_text, year, image_path, description) VALUES (?, ?, ?, ?, ?, ?)",
                      (cat_id, name, role_text, year, image_path, desc))
    conn.commit()
    # Ensure 2026 edition exists
    c.execute("SELECT 1 FROM editions WHERE year = 2026")
    if not c.fetchone():
        c.execute("INSERT INTO editions (year, title, tagline) VALUES (?, ?, ?)",
                  (2026, "Cookie Runners Golden Ballon d'Or 2026", "Every Cookie. Every Legend. One Golden Legacy."))
    conn.commit()
    conn.close()

def get_all_categories():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM categories ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_winners_for_category(cat_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM winners WHERE category_id = ? ORDER BY id", (cat_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_winners():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT w.*, c.name as category_name FROM winners w JOIN categories c ON w.category_id = c.id ORDER BY w.year DESC, w.id")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_winner(category_id, name, role_text, year, image_path, description):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO winners (category_id, name, role_text, year, image_path, description) VALUES (?, ?, ?, ?, ?, ?)",
              (category_id, name, role_text, year, image_path, description))
    conn.commit()
    wid = c.lastrowid
    conn.close()
    return wid

def get_moments():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM moments ORDER BY year DESC, id DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_moment(title, description, year):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO moments (title, description, year) VALUES (?, ?, ?)", (title, description, year))
    conn.commit()
    mid = c.lastrowid
    conn.close()
    return mid

def get_nominees():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM nominees ORDER BY year DESC, id DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_nominee(category_id, name, year, nominated_by):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO nominees (category_id, name, year, nominated_by) VALUES (?, ?, ?, ?)",
              (category_id, name, year, nominated_by))
    conn.commit()
    nid = c.lastrowid
    conn.close()
    return nid

def delete_nominee(nid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM nominees WHERE id = ?", (nid,))
    conn.commit()
    conn.close()

def delete_winner(wid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM winners WHERE id = ?", (wid,))
    conn.commit()
    conn.close()
