"""Entry point so ``python -m lilyverse`` works without installing the package."""

import sys

from lilyverse.cli import main

if __name__ == "__main__":
    sys.exit(main())
