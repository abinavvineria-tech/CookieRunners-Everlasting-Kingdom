#!/usr/bin/env python3
"""EverLink SSH — application entry point.

Usage:
    python3 run.py              # start the Flask GUI on localhost:5000
    python3 run.py --cli        # run the CLI (delegates to everlink.cli)
"""

from __future__ import annotations

import sys

from everlink.cli import main as cli_main
from everlink.web import create_app


def main() -> int:
    if len(sys.argv) > 1:
        return cli_main(sys.argv[1:])

    app = create_app()
    from everlink.config import load_settings
    settings = load_settings()
    host = settings.get("web_host", "127.0.0.1")
    port = settings.get("web_port", 5000)
    print(f"EverLink SSH GUI starting on http://{host}:{port}")
    print("Bind address is localhost-only by default. Do not expose to the network.")
    app.run(host=host, port=port, debug=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
