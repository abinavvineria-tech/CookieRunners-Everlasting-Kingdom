"""EVERLASTING BLOOM — Flask tribute application."""
import os
from flask import Flask, render_template, request, redirect, url_for, flash, g, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, init_db, seed_milestones

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.environ.get('EB_SECRET', 'everlasting-bloom-dev-key-change-in-production')

@app.before_request
def load_db():
    pass  # get_db handles per-request

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/legend')
def legend():
    db = get_db()
    milestones = db.execute("SELECT * FROM milestones WHERE category='Legend' ORDER BY date DESC").fetchall()
    return render_template('legend.html', milestones=milestones)

@app.route('/chronicles')
def chronicles():
    return render_template('chronicles.html')

@app.route('/timeline')
def timeline():
    db = get_db()
    milestones = db.execute("SELECT * FROM milestones ORDER BY date DESC").fetchall()
    return render_template('timeline.html', milestones=milestones)

@app.route('/garden', methods=['GET', 'POST'])
def garden():
    db = get_db()
    if request.method == 'POST':
        x = float(request.form.get('x', 50))
        y = float(request.form.get('y', 50))
        color = request.form.get('color', '#f0ebe4')
        db.execute("INSERT INTO garden_flowers (x, y, color) VALUES (?, ?, ?)", (x, y, color))
        db.commit()
    flowers = db.execute("SELECT * FROM garden_flowers ORDER BY created_at DESC LIMIT 50").fetchall()
    return render_template('garden.html', flowers=flowers)

@app.route('/letters', methods=['GET', 'POST'])
def letters():
    db = get_db()
    if request.method == 'POST':
        msg = request.form.get('message', '').strip()
        author = request.form.get('author', 'A Visitor').strip()
        if msg and len(msg) <= 1000 and len(author) <= 120:
            db.execute("INSERT INTO letters (message, author, approved) VALUES (?, ?, ?)", (msg, author, 0))
            db.commit()
            flash("Your letter has been submitted for moderation. Thank you.", "success")
        else:
            flash("Invalid input. Please check your message length.", "danger")
    approved = db.execute("SELECT * FROM letters WHERE approved=1 ORDER BY date_submitted DESC").fetchall()
    return render_template('letters.html', letters=approved)

@app.route('/memories')
def memories():
    db = get_db()
    milestones = db.execute("SELECT * FROM milestones WHERE category='Memory' ORDER BY date DESC").fetchall()
    return render_template('memories.html', milestones=milestones)

@app.route('/nexus')
def nexus():
    return render_template('nexus.html')

@app.route('/nexus-timeline')
def nexus_timeline():
    db = get_db()
    milestones = db.execute("SELECT * FROM milestones WHERE category='Timeline' ORDER BY date DESC").fetchall()
    return render_template('nexus_timeline.html', milestones=milestones)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        if request.method == 'POST':
            pw = request.form.get('password', '')
            if pw == os.environ.get('EB_ADMIN_PASSWORD', 'everbloom-admin-default-change'):
                session['admin'] = True
                flash("Welcome, moderator.", "success")
            else:
                flash("Invalid credentials.", "danger")
        return render_template('admin_login.html')
    db = get_db()
    if request.method == 'POST' and 'approve' in request.form:
        letter_id = request.form.get('approve')
        db.execute("UPDATE letters SET approved=1, moderated_by=1 WHERE id=?", (letter_id,))
        db.commit()
    pending = db.execute("SELECT * FROM letters WHERE approved=0 ORDER BY date_submitted DESC").fetchall()
    return render_template('admin.html', pending=pending)

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=False)
