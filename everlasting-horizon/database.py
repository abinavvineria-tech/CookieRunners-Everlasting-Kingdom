"""EVERLASTING HORIZON — Database layer.

Provides per-request SQLite connections, one-time schema initialisation and
friendly seed data. All seed content is original fan-created material for the
unofficial Everlasting Horizon fan project — it is not official Cookie Run
lore and is not affiliated with Devsisters.
"""
from flask import g
import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'everlasting_horizon.db')


def get_db():
    """Return the current request's SQLite connection, opening it on first use."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db


def close_db(exception):
    """Close the request's SQLite connection at teardown."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    """Initialise the database from schema.sql and seed friendly default data."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as f:
        conn.executescript(f.read())

    cur = conn.cursor()

    # --- Default project settings ---
    default_password = os.environ.get('EH_ADMIN_PASSWORD', 'everlasting-horizon-admin')
    settings = [
        ('site_name', 'Everlasting Horizon'),
        ('site_tagline', 'A New Journey. A New World. An Everlasting Dream.'),
        ('site_motto', 'One Run. One Dream. One United.'),
        ('about_text', 'Everlasting Horizon is an unofficial, fan-made digital universe celebrating friendship, creativity, adventures, memories, and the future of Cookie Run. Built with 🍪 by Cookie Runners, for Cookie Runners.'),
        ('primary_color', '#1e3a8a'),        # royal blue
        ('accent_color', '#d4af37'),         # gold
        ('magic_color', '#7c3aed'),          # magical purple
        ('admin_password_set', '1'),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", settings
    )

    # --- Default administrator account ---
    admin_pw_hash = generate_password_hash(default_password)
    cur.execute(
        "INSERT OR IGNORE INTO admin_users (username, password_hash, role) VALUES (?, ?, ?)",
        ('captain', admin_pw_hash, 'administrator'),
    )

    # --- Seed characters only if empty ---
    if cur.execute("SELECT COUNT(*) FROM characters").fetchone()[0] == 0:
        _seed_characters(cur)

    # --- Seed worlds only if empty ---
    if cur.execute("SELECT COUNT(*) FROM worlds").fetchone()[0] == 0:
        _seed_worlds(cur)

    # --- Seed adventures only if empty ---
    if cur.execute("SELECT COUNT(*) FROM adventures").fetchone()[0] == 0:
        _seed_adventures(cur)

    # --- Seed timeline events only if empty ---
    if cur.execute("SELECT COUNT(*) FROM timeline_events").fetchone()[0] == 0:
        _seed_timeline(cur)

    # --- Seed community members only if empty ---
    if cur.execute("SELECT COUNT(*) FROM community_members").fetchone()[0] == 0:
        _seed_community(cur)

    # --- Seed future projects only if empty ---
    if cur.execute("SELECT COUNT(*) FROM future_projects").fetchone()[0] == 0:
        _seed_future(cur)

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Seed data — all original fan creations
# ---------------------------------------------------------------------------

def _seed_characters(cur):
    characters = [
        # (name, title, role, description, history, personality, color, emoji, featured)
        (
            'Starlight Cookie', 'Guardian of the Night Sky', 'Wayfinder',
            'A brave cookie who charts the constellations and guides lost travelers home by starlight.',
            'Starlight Cookie fell from a shooting star into the Oven of Beginnings and has spent every dawn since mapping the skies above the kingdom.',
            'Courageous, curious, and always looking up. Starlight believes no horizon is too far to reach.',
            '#7c3aed', '✨', 1,
        ),
        (
            'Honeybun Cookie', 'Keeper of Sweet Memories', 'Baker',
            'A warm-hearted baker whose fresh-baked treats bring friends together around the table.',
            'Honeybun Cookie opened a little oven in the Golden Meadow and has never turned away a hungry friend.',
            'Gentle, generous, and the first to offer a hug — or a cookie — to anyone in need.',
            '#d4af37', '🍪', 1,
        ),
        (
            'Azure Cookie', 'Wave of the Royal Tide', 'Royal Guard',
            'A steadfast protector who watches over the kingdom shores with royal-blue pride.',
            'Azure Cookie was sworn to guard the coastline after a great storm, and stands watch to this day.',
            'Loyal, disciplined, and quietly kind beneath a serious exterior.',
            '#1e3a8a', '🌊', 1,
        ),
        (
            'Willow Cookie', 'Whisper of the Gentle Grove', 'Herbalist',
            'A soft-spoken herbalist who tends the grove and brews calming teas for weary travelers.',
            'Willow Cookie grew up among the ancient trees and learned to listen to what the leaves remember.',
            'Patient, observant, and deeply caring. Willow remembers every story ever shared in the grove.',
            '#f8fafc', '🌿', 0,
        ),
        (
            'Moonbeam Cookie', 'Dream of the Soft Slumber', 'Dreamweaver',
            'A gentle dreamweaver who spins peaceful nights and sweet dreams for every cookie in the kingdom.',
            'Moonbeam Cookie drifts between sleep and starlight, catching nightmares before they can trouble anyone.',
            'Calm, soothing, and always ready with a lullaby.',
            '#7c3aed', '🌙', 0,
        ),
    ]
    cur.executemany(
        """INSERT INTO characters
           (name, title, role, description, history, personality, color, image_emoji, is_featured)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        characters,
    )

    # Friendships between the seeded characters (ids 1..5 in insertion order)
    friendships = [
        (1, 2, 'Baked the first dawn biscuits together in the Golden Meadow.'),
        (3, 4, 'Guarded the grove through the spring bloom and shared many quiet mornings.'),
        (1, 5, 'Chart the constellations each night and weave starlight into sweet dreams.'),
    ]
    cur.executemany(
        """INSERT INTO friendships (character_a_id, character_b_id, moment)
           VALUES (?, ?, ?)""",
        friendships,
    )


def _seed_worlds(cur):
    worlds = [
        ('Oven of Beginnings', 'Where every journey starts with a single step into the warm, golden light.',
         'The Heartland', '#1e3a8a', '🍪', 1),
        ('Starlight Peaks', 'Mountaintops where constellations are born and wishes take flight into the night.',
         'The Highlands', '#7c3aed', '✨', 1),
        ('Crystal Caves', 'Glittering caverns that hold the kingdom\u2019s oldest memories and brightest secrets.',
         'The Depths', '#f8fafc', '💎', 0),
        ('Golden Meadow', 'Sun-drenched fields where friendship grows like wildflowers and laughter never fades.',
         'The Lowlands', '#d4af37', '🌼', 0),
    ]
    cur.executemany(
        """INSERT INTO worlds (name, description, region, color, image_emoji, is_featured)
           VALUES (?, ?, ?, ?, ?, ?)""",
        worlds,
    )

    stories = [
        # world_id 1 — Oven of Beginnings
        (1, 'The First Rise',
         'The oven breathed warmth into the world for the very first time, and from it stepped the first friends of the kingdom.',
         'Long before the stars had names, the Oven of Beginnings glowed with a gentle, patient heat. When the first cookie stepped out, the world was quiet and full of possibility. That first breath of warm air became the promise that every new start matters — no matter how small.'),
        (1, 'A Warm Welcome',
         'New travelers are always greeted with a fresh-baked cookie and a place to rest by the oven\u2019s glow.',
         'The bakers of the Oven of Beginnings believe that no one should arrive empty-handed. Every visitor receives a warm treat, a cup of tea, and a seat by the fire until they feel at home. It is a tradition older than the kingdom itself.'),
        # world_id 2 — Starlight Peaks
        (2, 'The Naming of the Stars',
         'Starlight Cookie climbed the highest peak and gave each twinkling light a name and a story.',
         'Up on Starlight Peaks the sky is so close you can almost reach it. Starlight Cookie made the long climb with nothing but a lantern and a notebook, returning with names for every constellation and a promise to keep watching over them.'),
        (2, 'The Wish Lantern Festival',
         'Each year the cookies release glowing lanterns that carry their hopes up to the highest peaks.',
         'When the lanterns rise, the whole kingdom glows. It is a night of quiet wishes, shared dreams, and the understanding that even the smallest light can travel very far.'),
        # world_id 3 — Crystal Caves
        (3, 'The Memory Crystal',
         'Deep inside the caves, a crystal holds echoes of every friendship ever formed in the kingdom.',
         'The Crystal Caves hum softly with forgotten songs and remembered laughter. Willow Cookie tends the largest crystal, adding a new shimmer whenever a new friendship is forged.'),
        # world_id 4 — Golden Meadow
        (4, 'The Great Meadow Picnic',
         'Every summer the whole kingdom gathers in the Golden Meadow for a day of games, treats, and togetherness.',
         'Blankets spread across the grass, honey-lemon tea in every cup, and laughter carried on the breeze. It is the day the kingdom remembers that friendship is its sweetest treasure.'),
    ]
    cur.executemany(
        """INSERT INTO stories (world_id, title, excerpt, content) VALUES (?, ?, ?, ?)""",
        stories,
    )


def _seed_adventures(cur):
    adventures = [
        ('The Starlight Climb', 'story',
         'Join Starlight Cookie on a journey up Starlight Peaks to find the brightest constellation.',
         'A shimmering star-chart', 'completed'),
        ('Bake-a-thon for Friends', 'quest',
         'Help Honeybun Cookie bake enough treats for the entire Golden Meadow picnic.',
         'A basket of warm cookies', 'open'),
        ('Tidewatch Patrol', 'story',
         'Azure Cookie keeps watch over the shoreline as the moon pulls the tide in and out.',
         'A seashell compass', 'open'),
        ('Grove Tea Ceremony', 'quest',
         'Gather calming herbs with Willow Cookie and brew tea for a weary traveler.',
         'A cup of grove tea', 'upcoming'),
        ('Dreamweaving Night', 'story',
         'Moonbeam Cookie spins peaceful dreams while the kingdom sleeps under a blanket of stars.',
         'A pouch of dream-dust', 'completed'),
        ('The Lost Constellation', 'quest',
         'Help Starlight Cookie find a constellation that has gone missing from the night sky.',
         'A rediscovered star', 'open'),
    ]
    cur.executemany(
        """INSERT INTO adventures (title, type, description, reward, status)
           VALUES (?, ?, ?, ?, ?)""",
        adventures,
    )


def _seed_timeline(cur):
    events = [
        ('The First Oven Lit', '2026-01-10', 'milestone',
         'The Everlasting Horizon project began with a single spark: the dream of a new Cookie Run universe.',
         'Fan project milestone'),
        ('Friendship Blooms in the Meadow', '2026-02-14', 'memory',
         'The first community gathering celebrated the friendships that make the kingdom feel like home.',
         'Community celebration'),
        ('Starlight Peaks Discovered', '2026-04-01', 'milestone',
         'Explorers charted the highlands and found the peaks where constellations are born.',
         'Fan-created world lore'),
        ('The Crystal Caves Opened', '2026-06-15', 'memory',
         'Travelers ventured into the caverns and returned with stories of glittering memories.',
         'Fan-created world lore'),
        ('Journey Timeline Launched', '2026-09-01', 'milestone',
         'The Journey Timeline was created to record milestones and plan the road ahead together.',
         'Feature launch'),
        ('Future Horizon Planning', '2027-03-01', 'future',
         'Upcoming projects and possibilities are being shaped by the Cookie Runners community.',
         'Community roadmap'),
    ]
    cur.executemany(
        """INSERT INTO timeline_events (title, event_date, category, description, source)
           VALUES (?, ?, ?, ?, ?)""",
        events,
    )


def _seed_community(cur):
    members = [
        ('Captain Abinav', 'Founder of Cookie Runners United',
         'Leading the crew with one dream: one run, one dream, one united.'),
        ('Shadow Milk Cookie', 'Head Coach & Strategist',
         'Guiding the team from the sidelines with wisdom and care.'),
        ('Moonlight Cookie', 'Creative Playmaker',
         'Bringing imagination and flair to every adventure on the field.'),
        ('A Fellow Cookie Runner', 'Community Storyteller',
         'Sharing memories that remind us why every journey matters.'),
    ]
    cur.executemany(
        """INSERT INTO community_members (name, contribution, message) VALUES (?, ?, ?)""",
        members,
    )


def _seed_future(cur):
    projects = [
        ('CookieVerse Expansion', 'New worlds and stories for every cookie to explore.', 'planned', 10, '2027-06-01'),
        ('Character Archives Deep Dive', 'Richer profiles, friendships, and memorable moments.', 'in-progress', 45, '2027-04-01'),
        ('Adventure Hub Quests', 'Interactive stories and creative quests for the community.', 'planned', 20, '2027-05-01'),
        ('Community Hall Celebration', 'A dedicated space to celebrate Cookie Runners and their creativity.', 'upcoming', 5, '2027-07-01'),
    ]
    cur.executemany(
        """INSERT INTO future_projects (title, description, status, progress, target_date)
           VALUES (?, ?, ?, ?, ?)""",
        projects,
    )
