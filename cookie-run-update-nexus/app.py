"""Cookie Run — Eternal Update Nexus.

An intelligent Cookie Run news researcher, update tracker, and personal
Cookie Runner assistant landing page.

Unofficial fan project — not affiliated with or endorsed by Devsisters Corporation.
"""

import os
from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "cookie-run-update-nexus"}, 200

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        port=int(os.environ.get("FLASK_PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true",
    )
