"""Top-level Flask entry point for local development.

Usage:
    python app.py

Then open http://127.0.0.1:5000

Debug mode is disabled by default. Set LILYVERSE_DEBUG=1 to enable it for
development only (never expose the dev server to the public internet).
"""

import os
import sys

# Allow running both from the repo root and after pip install -e .
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from lilyverse.web import create_app

app = create_app()

if __name__ == "__main__":
    debug = os.environ.get("LILYVERSE_DEBUG", "0") == "1"
    port = int(os.environ.get("LILYVERSE_PORT", "5000"))
    host = os.environ.get("LILYVERSE_HOST", "127.0.0.1")
    if debug:
        print("WARNING: Flask debug mode is ENABLED. Use only for local development.")
    app.run(host=host, port=port, debug=debug)
