#!/usr/bin/env python3
"""Entry point to run the Champions League Countdown Nexus backend."""
import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("DEBUG", "true").lower() == "true",
    )
