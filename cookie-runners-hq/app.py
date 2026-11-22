import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort

from database import (
    DB_PATH,
    init_db,
    seed_data,
    get_categories,
    get_category,
    get_games,
    get_game,
    add_game,
    update_game,
    delete_game,
    get_announcements,
    get_announcement,
    add_announcement,
    update_announcement,
    delete_announcement,
    get_updates,
    add_update,
    delete_update,
    get_events,
    add_event,
    delete_event,
    get_calendar_items,
    add_calendar_item,
    delete_calendar_item,
    get_dashboard_data,
    verify_user,
    GAME_STATUSES,
    CONFIRMATION_STATUSES,
    ANNOUNCEMENT_TYPES,
    CALENDAR_ITEM_TYPES,
)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-change-me-in-production"),
    )

    init_db()
    seed_data()

    # ---------------------------------------------------------------- public
    @app.route("/")
    def dashboard():
        data = get_dashboard_data()
        return render_template("dashboard.html", **data)

    @app.route("/games")
    def games_list():
        game_type = request.args.get("type")
        status = request.args.get("status")
        q = request.args.get("q")
        games = get_games(game_type=game_type, status=status, q=q)
        categories = get_categories()
        return render_template(
            "games.html",
            games=games,
            categories=categories,
            game_type=game_type,
            status=status,
            q=q,
            game_statuses=GAME_STATUSES,
        )

    @app.route("/games/<slug>")
    def game_detail(slug):
        game = get_game(slug)
        if not game:
            abort(404)
        updates = [u for u in get_updates(game_id=game["id"])]
        events = [e for e in get_events(game_id=game["id"])]
        return render_template(
            "game_detail.html",
            game=game,
            updates=updates,
            events=events,
        )

    @app.route("/tracker")
    def tracker():
        category = request.args.get("category")
        atype = request.args.get("type")
        conf = request.args.get("confirmation")
        q = request.args.get("q")
        announcements = get_announcements(
            category=category, atype=atype, conf=conf, q=q
        )
        categories = get_categories()
        return render_template(
            "tracker.html",
            announcements=announcements,
            categories=categories,
            announcement_types=ANNOUNCEMENT_TYPES,
            confirmation_statuses=CONFIRMATION_STATUSES,
            category=category,
            atype=atype,
            conf=conf,
            q=q,
        )

    @app.route("/tracker/<slug>")
    def announcement_detail(slug):
        announcement = get_announcement(slug)
        if not announcement:
            abort(404)
        return render_template("announcement_detail.html", announcement=announcement)

    @app.route("/upcoming")
    def upcoming():
        games = get_games()
        upcoming = [
            g for g in games
            if g["status"] in ("Officially announced", "In development", "Release date announced")
        ]
        return render_template("upcoming.html", games=upcoming, game_statuses=GAME_STATUSES)

    @app.route("/calendar")
    def calendar():
        import calendar as cal_module
        import datetime

        today = datetime.date.today()
        view = request.args.get("view", "month")
        try:
            year = int(request.args.get("year") or today.year)
            month = int(request.args.get("month") or today.month)
        except ValueError:
            year, month = today.year, today.month
        items = get_calendar_items(year=year, month=month, view=view)
        weeks = cal_module.monthcalendar(year, month)
        return render_template(
            "calendar.html",
            items=items,
            view=view,
            year=year,
            month=month,
            weeks=weeks,
            calendar_item_types=CALENDAR_ITEM_TYPES,
        )

    @app.route("/search")
    def search():
        q = request.args.get("q", "").strip()
        results = {"games": [], "announcements": [], "events": []}
        if q:
            results["games"] = get_games(q=q)
            results["announcements"] = get_announcements(q=q)
            all_events = get_events()
            q_lower = q.lower()
            results["events"] = [
                e for e in all_events
                if q_lower in (e.get("title") or "").lower()
                or q_lower in (e.get("description") or "").lower()
            ]
        return render_template("search.html", q=q, results=results)

    # ---------------------------------------------------------------- APIs
    @app.route("/api/games")
    def api_games():
        return jsonify({"games": get_games()})

    @app.route("/api/announcements")
    def api_announcements():
        return jsonify({"announcements": get_announcements()})

    @app.route("/api/events")
    def api_events():
        return jsonify({"events": get_events()})

    @app.route("/api/calendar")
    def api_calendar():
        return jsonify({"items": get_calendar_items()})

    # ---------------------------------------------------------------- admin
    def admin_required(f):
        from functools import wraps

        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get("admin_user"):
                flash("Administrator login required.", "warning")
                return redirect(url_for("admin_login", next=request.path))
            return f(*args, **kwargs)

        return decorated

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            user = verify_user(username, password)
            if user:
                session["admin_user"] = {
                    "id": user["id"],
                    "username": user["username"],
                    "role": user["role"],
                }
                flash("Welcome back, administrator.", "success")
                next_url = request.args.get("next") or url_for("admin_dashboard")
                return redirect(next_url)
            flash("Invalid username or password.", "danger")
        return render_template("admin_login.html")

    @app.route("/admin/logout")
    def admin_logout():
        session.pop("admin_user", None)
        flash("Logged out successfully.", "info")
        return redirect(url_for("dashboard"))

    @app.route("/admin")
    @admin_required
    def admin_dashboard():
        from database import get_dashboard_data
        data = get_dashboard_data()
        return render_template("admin_dashboard.html", **data)

    @app.route("/admin/games", methods=["GET", "POST"])
    @admin_required
    def admin_games():
        if request.method == "POST":
            data = _game_form_data()
            try:
                add_game(data)
                flash("Game added to the directory.", "success")
            except Exception as exc:  # noqa: BLE001
                flash(f"Could not add game: {exc}", "danger")
            return redirect(url_for("admin_games"))
        games = get_games()
        return render_template("admin_games.html", games=games, game_statuses=GAME_STATUSES)

    @app.route("/admin/games/<int:gid>/edit", methods=["GET", "POST"])
    @admin_required
    def admin_edit_game(gid):
        game = get_game_by_id(gid) if False else _get_game_row(gid)
        if not game:
            abort(404)
        if request.method == "POST":
            data = _game_form_data()
            try:
                update_game(gid, data)
                flash("Game updated.", "success")
            except Exception as exc:  # noqa: BLE001
                flash(f"Could not update game: {exc}", "danger")
            return redirect(url_for("admin_games"))
        return render_template("admin_edit_game.html", game=game, game_statuses=GAME_STATUSES)

    @app.route("/admin/games/<int:gid>/delete", methods=["POST"])
    @admin_required
    def admin_delete_game(gid):
        delete_game(gid)
        flash("Game removed from the directory.", "warning")
        return redirect(url_for("admin_games"))

    @app.route("/admin/announcements", methods=["GET", "POST"])
    @admin_required
    def admin_announcements():
        if request.method == "POST":
            data = _announcement_form_data()
            try:
                add_announcement(data)
                flash("Announcement published.", "success")
            except Exception as exc:  # noqa: BLE001
                flash(f"Could not publish announcement: {exc}", "danger")
            return redirect(url_for("admin_announcements"))
        announcements = get_announcements(published_only=False)
        categories = get_categories()
        return render_template(
            "admin_announcements.html",
            announcements=announcements,
            categories=categories,
            announcement_types=ANNOUNCEMENT_TYPES,
            confirmation_statuses=CONFIRMATION_STATUSES,
        )

    @app.route("/admin/announcements/<int:aid>/edit", methods=["GET", "POST"])
    @admin_required
    def admin_edit_announcement(aid):
        announcement = get_announcement_by_id(aid) if False else _get_announcement_row(aid)
        if not announcement:
            abort(404)
        if request.method == "POST":
            data = _announcement_form_data()
            try:
                update_announcement(aid, data)
                flash("Announcement updated.", "success")
            except Exception as exc:  # noqa: BLE001
                flash(f"Could not update announcement: {exc}", "danger")
            return redirect(url_for("admin_announcements"))
        categories = get_categories()
        return render_template(
            "admin_edit_announcement.html",
            announcement=announcement,
            categories=categories,
            announcement_types=ANNOUNCEMENT_TYPES,
            confirmation_statuses=CONFIRMATION_STATUSES,
        )

    @app.route("/admin/announcements/<int:aid>/delete", methods=["POST"])
    @admin_required
    def admin_delete_announcement(aid):
        delete_announcement(aid)
        flash("Announcement removed.", "warning")
        return redirect(url_for("admin_announcements"))

    @app.route("/admin/updates", methods=["GET", "POST"])
    @admin_required
    def admin_updates():
        if request.method == "POST":
            data = _update_form_data()
            try:
                add_update(data)
                flash("Game update added.", "success")
            except Exception as exc:  # noqa: BLE001
                flash(f"Could not add update: {exc}", "danger")
            return redirect(url_for("admin_updates"))
        updates = get_updates()
        games = get_games()
        return render_template(
            "admin_updates.html",
            updates=updates,
            games=games,
            confirmation_statuses=CONFIRMATION_STATUSES,
        )

    @app.route("/admin/updates/<int:uid>/delete", methods=["POST"])
    @admin_required
    def admin_delete_update(uid):
        delete_update(uid)
        flash("Update removed.", "warning")
        return redirect(url_for("admin_updates"))

    @app.route("/admin/events", methods=["GET", "POST"])
    @admin_required
    def admin_events():
        if request.method == "POST":
            data = _event_form_data()
            try:
                add_event(data)
                flash("Event added.", "success")
            except Exception as exc:  # noqa: BLE001
                flash(f"Could not add event: {exc}", "danger")
            return redirect(url_for("admin_events"))
        events = get_events()
        games = get_games()
        return render_template(
            "admin_events.html",
            events=events,
            games=games,
            confirmation_statuses=CONFIRMATION_STATUSES,
        )

    @app.route("/admin/events/<int:eid>/delete", methods=["POST"])
    @admin_required
    def admin_delete_event(eid):
        delete_event(eid)
        flash("Event removed.", "warning")
        return redirect(url_for("admin_events"))

    @app.route("/admin/calendar", methods=["GET", "POST"])
    @admin_required
    def admin_calendar():
        if request.method == "POST":
            data = _calendar_form_data()
            try:
                add_calendar_item(data)
                flash("Calendar item added.", "success")
            except Exception as exc:  # noqa: BLE001
                flash(f"Could not add calendar item: {exc}", "danger")
            return redirect(url_for("admin_calendar"))
        items = get_calendar_items()
        games = get_games()
        return render_template(
            "admin_calendar.html",
            items=items,
            games=games,
            calendar_item_types=CALENDAR_ITEM_TYPES,
            confirmation_statuses=CONFIRMATION_STATUSES,
        )

    @app.route("/admin/calendar/<int:cid>/delete", methods=["POST"])
    @admin_required
    def admin_delete_calendar_item(cid):
        delete_calendar_item(cid)
        flash("Calendar item removed.", "warning")
        return redirect(url_for("admin_calendar"))

    @app.route("/admin/categories", methods=["GET", "POST"])
    @admin_required
    def admin_categories():
        if request.method == "POST":
            name = (request.form.get("name") or "").strip()
            slug = (request.form.get("slug") or "").strip()
            desc = (request.form.get("description") or "").strip()
            color = (request.form.get("color") or "#8b5cf6").strip()
            if not name or not slug:
                flash("Name and slug are required.", "danger")
            else:
                _add_category(name, slug, desc, color)
                flash("Category added.", "success")
            return redirect(url_for("admin_categories"))
        categories = get_categories()
        return render_template("admin_categories.html", categories=categories)

    @app.route("/admin/categories/<int:cid>/delete", methods=["POST"])
    @admin_required
    def admin_delete_category(cid):
        from database import get_conn as _gc
        conn = _gc()
        conn.execute("DELETE FROM categories WHERE id = ?", (cid,))
        conn.commit()
        conn.close()
        flash("Category removed.", "warning")
        return redirect(url_for("admin_categories"))

    # ---------------------------------------------------------------- helpers
    def _get_game_row(gid):
        import sqlite3
        conn = sqlite3.connect(DB_PATH if "DB_PATH" in globals() else __import__("database").DB_PATH)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM games WHERE id = ?", (gid,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def _get_announcement_row(aid):
        import sqlite3
        from database import DB_PATH
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM announcements WHERE id = ?", (aid,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def _game_form_data():
        return {
            "title": (request.form.get("title") or "").strip(),
            "slug": (request.form.get("slug") or "").strip(),
            "description": request.form.get("description") or "",
            "short_description": (request.form.get("short_description") or "").strip(),
            "release_date": (request.form.get("release_date") or "") or None,
            "platforms": (request.form.get("platforms") or "").strip(),
            "developer": (request.form.get("developer") or "Devsisters").strip(),
            "publisher": (request.form.get("publisher") or "Devsisters").strip(),
            "official_website": (request.form.get("official_website") or "").strip(),
            "announcement_link": (request.form.get("announcement_link") or "").strip(),
            "trailer_url": (request.form.get("trailer_url") or "").strip(),
            "status": request.form.get("status") or "Released",
            "game_type": request.form.get("game_type") or "other",
            "featured": 1 if request.form.get("featured") else 0,
            "image_url": (request.form.get("image_url") or "").strip(),
            "confirmation_status": request.form.get("confirmation_status") or "confirmed",
            "notes": (request.form.get("notes") or "").strip(),
        }

    def _announcement_form_data():
        return {
            "title": (request.form.get("title") or "").strip(),
            "slug": (request.form.get("slug") or "").strip(),
            "summary": (request.form.get("summary") or "").strip(),
            "content": request.form.get("content") or "",
            "category_id": request.form.get("category_id", type=int),
            "announcement_type": request.form.get("announcement_type") or "news",
            "confirmation_status": request.form.get("confirmation_status") or "confirmed",
            "source_url": (request.form.get("source_url") or "").strip(),
            "source_name": (request.form.get("source_name") or "").strip(),
            "published_at": (request.form.get("published_at") or "") or None,
            "is_pinned": 1 if request.form.get("is_pinned") else 0,
            "is_published": 1 if request.form.get("is_published") else 0,
        }

    def _update_form_data():
        return {
            "game_id": request.form.get("game_id", type=int),
            "title": (request.form.get("title") or "").strip(),
            "version": (request.form.get("version") or "").strip(),
            "patch_notes": request.form.get("patch_notes") or "",
            "release_date": (request.form.get("release_date") or "") or None,
            "maintenance": 1 if request.form.get("maintenance") else 0,
            "source_url": (request.form.get("source_url") or "").strip(),
            "confirmation_status": request.form.get("confirmation_status") or "confirmed",
        }

    def _event_form_data():
        return {
            "game_id": request.form.get("game_id", type=int),
            "title": (request.form.get("title") or "").strip(),
            "description": request.form.get("description") or "",
            "start_date": (request.form.get("start_date") or "") or None,
            "end_date": (request.form.get("end_date") or "") or None,
            "event_type": request.form.get("event_type") or "event",
            "image_url": (request.form.get("image_url") or "").strip(),
            "source_url": (request.form.get("source_url") or "").strip(),
            "confirmation_status": request.form.get("confirmation_status") or "confirmed",
        }

    def _calendar_form_data():
        return {
            "title": (request.form.get("title") or "").strip(),
            "description": request.form.get("description") or "",
            "item_type": request.form.get("item_type") or "announcement",
            "start_date": (request.form.get("start_date") or "") or None,
            "end_date": (request.form.get("end_date") or "") or None,
            "all_day": 1 if request.form.get("all_day") else 0,
            "game_id": request.form.get("game_id", type=int),
            "url": (request.form.get("url") or "").strip(),
            "confirmation_status": request.form.get("confirmation_status") or "confirmed",
        }

    def _add_category(name, slug, desc, color):
        import sqlite3
        from database import DB_PATH
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO categories (name, slug, description, color) VALUES (?, ?, ?, ?)",
            (name, slug, desc, color),
        )
        conn.commit()
        conn.close()

    # expose DB_PATH for helper fallbacks
    from database import DB_PATH  # noqa: E402

    app.db_path = DB_PATH

    # ---------------------------------------------------------------- errors
    @app.errorhandler(404)
    def not_found(err):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(err):
        return render_template("500.html"), 500

    return app


app = create_app()

if __name__ == "__main__":
    # debug=False: the Werkzeug reloader is incompatible with this toolchain's
    # multiprocessing build; the app is fully tested via Flask's test client.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
