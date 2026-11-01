CREATE TABLE IF NOT EXISTS milestones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT,
    category TEXT CHECK(category IN ('Legend','Chronicle','Memory','Timeline')),
    character TEXT NOT NULL,
    source TEXT CHECK(source IN ('Official fact','Verified canon','Personal memory','Fan interpretation')),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS letters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    author TEXT NOT NULL,
    date_submitted TEXT DEFAULT CURRENT_TIMESTAMP,
    approved INTEGER DEFAULT 0,
    moderated_by INTEGER DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS garden_flowers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    x REAL,
    y REAL,
    color TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'moderator'
);
