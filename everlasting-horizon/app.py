"""EVERLASTING HORIZON — Flask application.

An unofficial, fan-made Cookie Run-inspired digital universe.
All features are functional and backed by persistent SQLite storage.
"""
import os
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, abort, g,
)
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db, close_db, init_db

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.environ.get(
    'EH_SECRET_KEY', 'everlasting-horizon-dev-key-change-in-production'
)
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'everlasting_horizon.db')

app.teardown_appcontext(close_db)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_setting(key, default=None):
    """Return a single setting value from the database."""
    db = get_db()
    row = db.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    return row['value'] if row else default


def all_settings():
    """Return every setting as a dict."""
    db = get_db()
    rows = db.execute("SELECT key, value FROM settings").fetchall()
    return {row['key']: row['value'] for row in rows}


def login_required(view):
    """Decorator protecting administrative routes."""

    def wrapped(*args, **kwargs):
        if not session.get('admin'):
            flash("Please sign in to access the administration area.", "warning")
            return redirect(url_for('admin_login', next=request.path))
        return view(*args, **kwargs)

    wrapped.__name__ = view.__name__
    return wrapped


def user_login_required(view):
    """Decorator protecting routes that require a signed-in website user."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in to continue.", "warning")
            return redirect(url_for('login', next=request.path))
        return view(*args, **kwargs)

    wrapped.__name__ = view.__name__
    return wrapped


def current_user():
    """Return the signed-in user row, or None."""
    if 'user_id' not in session:
        return None
    db = get_db()
    return db.execute(
        "SELECT id, username, email, role, created_at FROM users WHERE id = ?",
        (session['user_id'],),
    ).fetchone()


@app.context_processor
def inject_settings_and_user():
    """Make site settings and the current user available to every template."""
    return dict(settings=all_settings(), current_user=current_user())


# ---------------------------------------------------------------------------
# Public routes
# ---------------------------------------------------------------------------

@app.route('/')
def home():
    db = get_db()
    featured_characters = db.execute(
        "SELECT * FROM characters WHERE is_featured = 1 ORDER BY created_at DESC"
    ).fetchall()
    featured_worlds = db.execute(
        "SELECT * FROM worlds WHERE is_featured = 1 ORDER BY created_at DESC"
    ).fetchall()
    recent_timeline = db.execute(
        "SELECT * FROM timeline_events ORDER BY event_date DESC LIMIT 5"
    ).fetchall()
    open_adventures = db.execute(
        "SELECT * FROM adventures WHERE status = 'open' ORDER BY created_at DESC LIMIT 4"
    ).fetchall()
    return render_template(
        'home.html',
        characters=featured_characters,
        worlds=featured_worlds,
        timeline=recent_timeline,
        adventures=open_adventures,
    )


@app.route('/cookieverse')
def cookieverse():
    db = get_db()
    worlds = db.execute(
        "SELECT * FROM worlds ORDER BY is_featured DESC, created_at DESC"
    ).fetchall()
    stories = db.execute(
        "SELECT s.*, w.name AS world_name FROM stories s "
        "JOIN worlds w ON s.world_id = w.id ORDER BY s.created_at DESC"
    ).fetchall()
    return render_template('cookieverse.html', worlds=worlds, stories=stories)


@app.route('/characters')
def characters():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM characters ORDER BY is_featured DESC, name ASC"
    ).fetchall()
    return render_template('characters.html', characters=rows)


@app.route('/characters/<int:character_id>')
def character_detail(character_id):
    db = get_db()
    character = db.execute(
        "SELECT * FROM characters WHERE id = ?", (character_id,)
    ).fetchone()
    if character is None:
        abort(404)
    friendships = db.execute(
        """SELECT f.id, f.character_a_id, f.character_b_id, f.moment,
                  ca.name AS a_name, cb.name AS b_name
           FROM friendships f
           JOIN characters ca ON f.character_a_id = ca.id
           JOIN characters cb ON f.character_b_id = cb.id
           WHERE f.character_a_id = ? OR f.character_b_id = ?
           ORDER BY f.created_at DESC""",
        (character_id, character_id),
    ).fetchall()
    # Build a list of the friend (the other character in each friendship)
    friends = []
    for f in friendships:
        other_id = f['character_b_id'] if f['character_a_id'] == character_id else f['character_a_id']
        other = db.execute(
            "SELECT * FROM characters WHERE id = ?", (other_id,)
        ).fetchone()
        friends.append({'moment': f['moment'], 'friend': other})
    return render_template('character_detail.html',
                           character=character, friends=friends)


@app.route('/timeline')
def timeline():
    db = get_db()
    events = db.execute(
        "SELECT * FROM timeline_events ORDER BY event_date DESC"
    ).fetchall()
    return render_template('timeline.html', events=events)


@app.route('/adventures')
def adventures():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM adventures ORDER BY created_at DESC"
    ).fetchall()
    return render_template('adventures.html', adventures=rows)


@app.route('/adventures/<int:adventure_id>')
def adventure_detail(adventure_id):
    db = get_db()
    adventure = db.execute(
        "SELECT * FROM adventures WHERE id = ?", (adventure_id,)
    ).fetchone()
    if adventure is None:
        abort(404)
    return render_template('adventure_detail.html', adventure=adventure)


@app.route('/community')
def community():
    db = get_db()
    members = db.execute(
        "SELECT * FROM community_members ORDER BY join_date DESC"
    ).fetchall()
    return render_template('community.html', members=members)


@app.route('/future')
def future():
    db = get_db()
    projects = db.execute(
        "SELECT * FROM future_projects ORDER BY created_at DESC"
    ).fetchall()
    return render_template('future.html', projects=projects)


@app.route('/about')
def about():
    return render_template('about.html')


# ---------------------------------------------------------------------------
# Public authentication
# ---------------------------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Create a new website account."""
    if 'user_id' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')

        if not username or not email or not password:
            flash("Username, email and password are required.", "danger")
        elif password != confirm:
            flash("Passwords do not match.", "danger")
        elif len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
        else:
            db = get_db()
            if db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
                flash("That username is already taken.", "danger")
            elif db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone():
                flash("That email is already registered.", "danger")
            else:
                pw_hash = generate_password_hash(password)
                db.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, pw_hash),
                )
                db.commit()
                flash("Account created — welcome to Everlasting Horizon! Please sign in.", "success")
                return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Sign a website user in."""
    if 'user_id' in session:
        return redirect(url_for('profile'))
    next_url = request.args.get('next') or url_for('profile')
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['user_role'] = user['role']
            flash("Welcome back, " + user['username'] + ".", "success")
            return redirect(next_url)
        flash("Invalid username or password.", "danger")
    return render_template('login.html', next_url=next_url)


@app.route('/logout')
def logout():
    """Sign the current user out."""
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('user_role', None)
    flash("You have been signed out.", "info")
    return redirect(url_for('home'))


@app.route('/profile')
@user_login_required
def profile():
    """View the signed-in user's profile."""
    db = get_db()
    user = db.execute(
        "SELECT id, username, email, role, created_at FROM users WHERE id = ?",
        (session['user_id'],),
    ).fetchone()
    return render_template('profile.html', user=user)


# ---------------------------------------------------------------------------
# Administration
# ---------------------------------------------------------------------------

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin'):
        return redirect(url_for('admin_dashboard'))
    next_url = request.args.get('next') or url_for('admin_dashboard')
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        db = get_db()
        user = db.execute(
            "SELECT * FROM admin_users WHERE username = ?", (username,)
        ).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session['admin'] = True
            session['admin_username'] = user['username']
            flash("Welcome back, administrator.", "success")
            return redirect(next_url)
        flash("Invalid username or password.", "danger")
    return render_template('admin/login.html', next_url=next_url)


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    session.pop('admin_username', None)
    flash("You have been signed out.", "info")
    return redirect(url_for('home'))


@app.route('/admin/')
@login_required
def admin_dashboard():
    db = get_db()
    counts = {
        'characters': db.execute("SELECT COUNT(*) FROM characters").fetchone()[0],
        'worlds': db.execute("SELECT COUNT(*) FROM worlds").fetchone()[0],
        'stories': db.execute("SELECT COUNT(*) FROM stories").fetchone()[0],
        'adventures': db.execute("SELECT COUNT(*) FROM adventures").fetchone()[0],
        'timeline_events': db.execute("SELECT COUNT(*) FROM timeline_events").fetchone()[0],
        'community_members': db.execute("SELECT COUNT(*) FROM community_members").fetchone()[0],
        'future_projects': db.execute("SELECT COUNT(*) FROM future_projects").fetchone()[0],
    }
    recent = db.execute(
        "SELECT * FROM timeline_events ORDER BY created_at DESC LIMIT 5"
    ).fetchall()
    return render_template('admin/dashboard.html', counts=counts, recent=recent)


# ---- Characters (CRUD) ----

@app.route('/admin/characters')
@login_required
def admin_characters():
    db = get_db()
    rows = db.execute("SELECT * FROM characters ORDER BY name ASC").fetchall()
    return render_template('admin/characters.html', characters=rows)


@app.route('/admin/characters/new', methods=['GET', 'POST'])
@login_required
def admin_character_new():
    db = get_db()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        title = request.form.get('title', '').strip()
        role = request.form.get('role', '').strip()
        description = request.form.get('description', '').strip()
        history = request.form.get('history', '').strip()
        personality = request.form.get('personality', '').strip()
        color = request.form.get('color', '#1e3a8a').strip()
        emoji = request.form.get('image_emoji', '🍪').strip()
        featured = 1 if request.form.get('is_featured') else 0
        if not name or not title or not role or not description:
            flash("Name, title, role and description are required.", "danger")
            return render_template('admin/character_form.html',
                                   character=None, action=url_for('admin_character_new'))
        db.execute(
            """INSERT INTO characters
               (name, title, role, description, history, personality, color, image_emoji, is_featured)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, title, role, description, history, personality, color, emoji, featured),
        )
        db.commit()
        flash(f"Character '{name}' was added to the archives.", "success")
        return redirect(url_for('admin_characters'))
    return render_template('admin/character_form.html',
                           character=None, action=url_for('admin_character_new'))


@app.route('/admin/characters/<int:character_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_character_edit(character_id):
    db = get_db()
    character = db.execute(
        "SELECT * FROM characters WHERE id = ?", (character_id,)
    ).fetchone()
    if character is None:
        abort(404)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        title = request.form.get('title', '').strip()
        role = request.form.get('role', '').strip()
        description = request.form.get('description', '').strip()
        history = request.form.get('history', '').strip()
        personality = request.form.get('personality', '').strip()
        color = request.form.get('color', '#1e3a8a').strip()
        emoji = request.form.get('image_emoji', '🍪').strip()
        featured = 1 if request.form.get('is_featured') else 0
        if not name or not title or not role or not description:
            flash("Name, title, role and description are required.", "danger")
            return render_template('admin/character_form.html',
                                   character=character,
                                   action=url_for('admin_character_edit', character_id=character_id))
        db.execute(
            """UPDATE characters
               SET name=?, title=?, role=?, description=?, history=?, personality=?,
                   color=?, image_emoji=?, is_featured=?
               WHERE id=?""",
            (name, title, role, description, history, personality, color, emoji, featured, character_id),
        )
        db.commit()
        flash(f"Character '{name}' was updated.", "success")
        return redirect(url_for('admin_characters'))
    return render_template('admin/character_form.html',
                           character=character,
                           action=url_for('admin_character_edit', character_id=character_id))


@app.route('/admin/characters/<int:character_id>/delete', methods=['POST'])
@login_required
def admin_character_delete(character_id):
    db = get_db()
    character = db.execute(
        "SELECT name FROM characters WHERE id = ?", (character_id,)
    ).fetchone()
    if character is None:
        abort(404)
    db.execute("DELETE FROM characters WHERE id = ?", (character_id,))
    db.commit()
    flash(f"Character '{character['name']}' was removed from the archives.", "info")
    return redirect(url_for('admin_characters'))


# ---- Timeline events (CRUD) ----

@app.route('/admin/timeline')
@login_required
def admin_timeline():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM timeline_events ORDER BY event_date DESC"
    ).fetchall()
    return render_template('admin/timeline.html', events=rows)


@app.route('/admin/timeline/new', methods=['GET', 'POST'])
@login_required
def admin_timeline_new():
    db = get_db()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        event_date = request.form.get('event_date', '').strip()
        category = request.form.get('category', 'milestone').strip()
        description = request.form.get('description', '').strip()
        source = request.form.get('source', 'Fan project').strip()
        if not title or not event_date or not description:
            flash("Title, date and description are required.", "danger")
            return render_template('admin/timeline_form.html', event=None,
                                   action=url_for('admin_timeline_new'))
        db.execute(
            """INSERT INTO timeline_events
               (title, event_date, category, description, source)
               VALUES (?, ?, ?, ?, ?)""",
            (title, event_date, category, description, source),
        )
        db.commit()
        flash(f"Timeline event '{title}' was recorded.", "success")
        return redirect(url_for('admin_timeline'))
    return render_template('admin/timeline_form.html', event=None,
                           action=url_for('admin_timeline_new'))


@app.route('/admin/timeline/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_timeline_edit(event_id):
    db = get_db()
    event = db.execute(
        "SELECT * FROM timeline_events WHERE id = ?", (event_id,)
    ).fetchone()
    if event is None:
        abort(404)
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        event_date = request.form.get('event_date', '').strip()
        category = request.form.get('category', 'milestone').strip()
        description = request.form.get('description', '').strip()
        source = request.form.get('source', 'Fan project').strip()
        if not title or not event_date or not description:
            flash("Title, date and description are required.", "danger")
            return render_template('admin/timeline_form.html', event=event,
                                   action=url_for('admin_timeline_edit', event_id=event_id))
        db.execute(
            """UPDATE timeline_events
               SET title=?, event_date=?, category=?, description=?, source=?
               WHERE id=?""",
            (title, event_date, category, description, source, event_id),
        )
        db.commit()
        flash(f"Timeline event '{title}' was updated.", "success")
        return redirect(url_for('admin_timeline'))
    return render_template('admin/timeline_form.html', event=event,
                           action=url_for('admin_timeline_edit', event_id=event_id))


@app.route('/admin/timeline/<int:event_id>/delete', methods=['POST'])
@login_required
def admin_timeline_delete(event_id):
    db = get_db()
    event = db.execute(
        "SELECT title FROM timeline_events WHERE id = ?", (event_id,)
    ).fetchone()
    if event is None:
        abort(404)
    db.execute("DELETE FROM timeline_events WHERE id = ?", (event_id,))
    db.commit()
    flash(f"Timeline event '{event['title']}' was removed.", "info")
    return redirect(url_for('admin_timeline'))


# ---- Settings ----

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    db = get_db()
    if request.method == 'POST':
        updates = []
        for key in ('site_name', 'site_tagline', 'site_motto', 'about_text',
                    'primary_color', 'accent_color', 'magic_color'):
            value = request.form.get(key, '').strip()
            if key in ('primary_color', 'accent_color', 'magic_color'):
                # Basic colour validation: must look like a hex colour.
                import re
                if not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value):
                    flash(f"The colour for {key} must be a valid hex code (e.g. #1e3a8a).", "danger")
                    return redirect(url_for('admin_settings'))
            updates.append((value, key))
        db.executemany("UPDATE settings SET value = ? WHERE key = ?", updates)
        db.commit()
        flash("Project settings were updated.", "success")
        return redirect(url_for('admin_settings'))
    settings = all_settings()
    return render_template('admin/settings.html', settings=settings)


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=False)
