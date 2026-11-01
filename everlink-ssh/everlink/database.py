"""SQLite storage for host profiles and non-secret metadata.

No passwords or private keys are ever stored here. Only profile metadata,
timestamps, and limited diagnostic history.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .config import app_data_dir, database_path

SCHEMA = """
CREATE TABLE IF NOT EXISTS hosts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    hostname TEXT NOT NULL,
    username TEXT NOT NULL,
    port INTEGER NOT NULL DEFAULT 22,
    identity_file TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS connection_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_name TEXT,
    target TEXT NOT NULL,
    status TEXT NOT NULL,
    message TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    fingerprint TEXT,
    created_at TEXT NOT NULL
);
"""


def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    if db_path is None:
        db_path = database_path()
    else:
        db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    app_data_dir().mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Optional[Path] = None) -> None:
    conn = get_connection(db_path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---- hosts ----

def add_host(conn, name, hostname, username, port, identity_file=None) -> int:
    now = _now()
    cur = conn.execute(
        "INSERT INTO hosts (name, hostname, username, port, identity_file, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, hostname, username, port, identity_file, now, now),
    )
    conn.commit()
    return cur.lastrowid


def get_host(conn, name):
    return conn.execute("SELECT * FROM hosts WHERE name = ?", (name,)).fetchone()


def get_host_by_id(conn, host_id):
    return conn.execute("SELECT * FROM hosts WHERE id = ?", (host_id,)).fetchone()


def list_hosts(conn, search=None):
    if search:
        like = f"%{search}%"
        return conn.execute(
            "SELECT * FROM hosts WHERE name LIKE ? OR hostname LIKE ? OR username LIKE ? "
            "ORDER BY name",
            (like, like, like),
        ).fetchall()
    return conn.execute("SELECT * FROM hosts ORDER BY name").fetchall()


def update_host(conn, host_id, **fields) -> None:
    allowed = {"name", "hostname", "username", "port", "identity_file"}
    sets = []
    params = []
    for key, val in fields.items():
        if key in allowed:
            sets.append(f"{key} = ?")
            params.append(val)
    if not sets:
        return
    sets.append("updated_at = ?")
    params.append(_now())
    params.append(host_id)
    conn.execute(f"UPDATE hosts SET {', '.join(sets)} WHERE id = ?", params)
    conn.commit()


def delete_host(conn, host_id) -> None:
    conn.execute("DELETE FROM hosts WHERE id = ?", (host_id,))
    conn.commit()


# ---- connection attempts ----

def record_attempt(conn, profile_name, target, status, message=None) -> None:
    conn.execute(
        "INSERT INTO connection_attempts (profile_name, target, status, message, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (profile_name, target, status, message, _now()),
    )
    conn.commit()


def recent_attempts(conn, limit=10):
    return conn.execute(
        "SELECT * FROM connection_attempts ORDER BY created_at DESC LIMIT ?",
        (limit,),
    ).fetchall()


# ---- keys ----

def add_key(conn, name, path, fingerprint=None) -> None:
    conn.execute(
        "INSERT INTO keys (name, path, fingerprint, created_at) VALUES (?, ?, ?, ?)",
        (name, path, fingerprint, _now()),
    )
    conn.commit()


def list_keys_db(conn):
    return conn.execute("SELECT * FROM keys ORDER BY name").fetchall()
