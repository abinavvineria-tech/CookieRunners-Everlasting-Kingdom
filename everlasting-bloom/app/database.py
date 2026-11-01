"""EVERLASTING BLOOM — Database layer."""
from flask import g
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'everlasting_bloom.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as f:
        conn.executescript(f.read())
    # Seed core data if empty
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM letters")
    if cur.fetchone()[0] == 0:
        seed_letters(cur)
    cur.execute("SELECT COUNT(*) FROM milestones")
    if cur.fetchone()[0] == 0:
        seed_milestones(cur)
    conn.commit()
    conn.close()

def seed_letters(cur):
    letters = [
        ("Kindness is the root from which every bloom grows.", "A Visitor", "2026-08-10", 1, 1),
        ("Some flowers never stop blooming in our memories.", "Lily Friend", "2026-08-11", 1, 1),
        ("May her petals remind us to walk with integrity and compassion.", "A Friend", "2026-08-12", 1, 1),
    ]
    cur.executemany("INSERT INTO letters (message, author, date_submitted, approved, moderated_by) VALUES (?, ?, ?, ?, ?)", letters)

def seed_milestones(cur):
    milestones = [
        ("White Lily Cookie's first appearance in Cookie Run: Kingdom lore", "2023-01-15", "Legend", "White Lily Cookie", "Official fact"),
        ("Pure Vanilla Cookie and White Lily form their enduring friendship", "2024-03-20", "Chronicle", "Pure Vanilla Cookie", "Verified canon"),
        ("White Lily's journey reaches its most poignant chapter", "2025-11-30", "Legend", "White Lily Cookie", "Verified canon"),
        ("Community remembrance and tribute events begin", "2026-03-11", "Memory", "White Lily Cookie", "Personal memory"),
        ("EVERLASTING BLOOM tribute launched — August 12, 2026 highlighted", "2026-08-12", "Memory", "White Lily Cookie", "Fan interpretation"),
    ]
    cur.executemany("INSERT INTO milestones (title, date, category, character, source) VALUES (?, ?, ?, ?, ?)", milestones)
