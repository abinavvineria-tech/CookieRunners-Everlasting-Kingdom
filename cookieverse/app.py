from flask import Flask
from database import init_db, seed_first_edition
from routes import register_routes

def create_app(config_name="default"):
    import os
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="cookie-runners-golden-ballon-dor-2026-secret",
        DATABASE=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cookieverse.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    # Initialize DB
    init_db()
    seed_first_edition()  # ensures 2026 winners never overwritten accidentally
    register_routes(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
