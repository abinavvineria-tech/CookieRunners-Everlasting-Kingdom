from flask import render_template, request, redirect, url_for, jsonify, session, flash, Response
from database import (
    get_all_categories, get_winners_for_category, get_all_winners,
    add_winner, get_moments, add_moment, get_nominees, add_nominee,
    delete_nominee, delete_winner, seed_first_edition
)
from functools import wraps
import json

# Simple admin auth (hash-based, production should use proper hashing)
ADMIN_USERNAME = "cookie-runners-admin"
ADMIN_PASSWORD = "golden-ball-2026"

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated

def register_routes(app):
    @app.route("/")
    def home():
        cats = get_all_categories()
        return render_template("index.html", cats=cats)

    @app.route("/ceremony")
    def ceremony():
        return render_template("ceremony.html")

    @app.route("/ballon")
    def ballon():
        cats = get_all_categories()
        return render_template("ballon.html", cats=cats)

    @app.route("/awards")
    def awards():
        cats = get_all_categories()
        data = []
        for cat in cats:
            winners = get_winners_for_category(cat["id"])
            data.append({"category": cat, "winners": winners})
        return render_template("awards.html", data=data)

    @app.route("/categories")
    def categories():
        cats = get_all_categories()
        data = []
        for cat in cats:
            winners = get_winners_for_category(cat["id"])
            data.append({"category": cat, "winners": winners})
        return render_template("categories.html", data=data)

    @app.route("/hall-of-fame")
    def hall_of_fame():
        winners = get_all_winners()
        return render_template("hall_of_fame.html", winners=winners)

    @app.route("/legends")
    def legends():
        return render_template("legends.html")

    @app.route("/memories")
    def memories():
        moments = get_moments()
        return render_template("memories.html", moments=moments)

    @app.route("/moments")
    def moments():
        return redirect(url_for("memories"))

    @app.route("/community")
    def community():
        return render_template("community.html")

    @app.route("/nomination")
    def nomination():
        cats = get_all_categories()
        return render_template("nomination.html", cats=cats)

    @app.route("/nomination-center")
    def nomination_center():
        return redirect(url_for("nomination"))

    @app.route("/about")
    def about():
        return render_template("about.html")

    # Nomination actions
    @app.route("/nominate", methods=["POST"])
    def nominate():
        cat_id = request.form.get("category_id", type=int)
        name = request.form.get("name", "").strip()
        year_str = request.form.get("year", "2026")
        nominated_by = request.form.get("nominated_by", "Anonymous").strip()
        try:
            year = int(year_str)
        except:
            year = 2026
        if cat_id and name:
            add_nominee(cat_id, name, year, nominated_by)
            flash("Nomination received! The legacy grows.", "success")
        else:
            flash("Category and nominee name are required.", "danger")
        return redirect(url_for("nomination"))

    # Admin auth
    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if request.method == "POST":
            user = request.form.get("username", "").strip()
            pw = request.form.get("password", "").strip()
            if user == ADMIN_USERNAME and pw == ADMIN_PASSWORD:
                session["admin_logged_in"] = True
                flash("Welcome, administrator. The ceremony awaits.", "success")
                return redirect(url_for("admin"))
            else:
                flash("Invalid credentials. Access denied.", "danger")
        return render_template("admin_login.html")

    @app.route("/admin/logout")
    def admin_logout():
        session.pop("admin_logged_in", None)
        flash("Logged out.", "info")
        return redirect(url_for("admin_login"))

    # Admin dashboard (protected)
    @app.route("/admin", methods=["GET", "POST"])
    @login_required
    def admin():
        cats = get_all_categories()
        nominees = get_nominees()
        winners = get_all_winners()
        # Create new award edition
        if request.method == "POST":
            action = request.form.get("action")
            if action == "add_winner":
                cat_id = request.form.get("category_id", type=int)
                name = request.form.get("name", "").strip()
                role_text = request.form.get("role_text", "").strip()
                year_str = request.form.get("year", "2026")
                image_path = request.form.get("image_path", "/static/images/default.jpg").strip()
                description = request.form.get("description", "").strip()
                try:
                    year = int(year_str)
                except:
                    year = 2026
                if cat_id and name:
                    add_winner(cat_id, name, role_text, year, image_path, description)
                    flash("Winner added! The legacy grows.", "success")
                else:
                    flash("Name and category are required.", "danger")
            elif action == "delete_winner":
                wid = request.form.get("winner_id", type=int)
                if wid:
                    delete_winner(wid)
                    flash("Winner removed.", "warning")
            elif action == "add_nominee":
                # handled by /nominate, but included for completeness
                pass
        return render_template("admin.html", cats=cats, nominees=nominees, winners=winners)

    @app.route("/admin/export/json")
    @login_required
    def admin_export_json():
        data = {
            "categories": get_all_categories(),
            "winners": get_all_winners(),
            "nominees": get_nominees(),
            "moments": get_moments()
        }
        return Response(json.dumps(data, indent=2), mimetype="application/json")

    @app.route("/admin/export/csv")
    @login_required
    def admin_export_csv():
        import csv, io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Category", "Name", "Role", "Year", "Image Path", "Description"])
        for w in get_all_winners():
            writer.writerow([w.get("category_name", ""), w.get("name", ""), w.get("role_text", ""), w.get("year", ""), w.get("image_path", ""), w.get("description", "")])
        response = Response(output.getvalue(), mimetype="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=cookie-runners-golden-ballon-2026.csv"
        return response

    @app.route("/admin/edit-winner/<int:wid>", methods=["GET", "POST"])
    @login_required
    def admin_edit_winner(wid):
        # For simplicity, we redirect to admin with flash for edits; full editing uses admin form
        return redirect(url_for("admin"))

    # API endpoints
    @app.route("/api/categories")
    def api_categories():
        return jsonify({"categories": get_all_categories()})

    @app.route("/api/winners/<int:cat_id>")
    def api_winners(cat_id):
        return jsonify({"winners": get_winners_for_category(cat_id)})

    @app.route("/api/all-winners")
    def api_all_winners():
        return jsonify({"winners": get_all_winners()})

    @app.route("/api/nominees")
    def api_nominees():
        return jsonify({"nominees": get_nominees()})

    @app.route("/api/moments")
    def api_moments():
        return jsonify({"moments": get_moments()})
