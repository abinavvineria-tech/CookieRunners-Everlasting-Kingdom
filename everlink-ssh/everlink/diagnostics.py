"""Doctor diagnostics: Python, OpenSSH, permissions, and dependencies."""

from __future__ import annotations

import os
import shutil
import stat
import sys
from pathlib import Path

from .config import (
    app_config_dir,
    app_data_dir,
    database_path,
    config_path,
    VERSION,
)
from .ssh_manager import ssh_available, ssh_keygen_available


def python_info() -> dict:
    return {
        "executable": sys.executable,
        "version": ".".join(map(str, sys.version_info[:3])),
        "full": sys.version,
    }


def openssh_info() -> dict:
    return {
        "ssh": shutil.which("ssh"),
        "ssh-keygen": shutil.which("ssh-keygen"),
        "ssh-add": shutil.which("ssh-add"),
        "ssh_available": ssh_available(),
        "keygen_available": ssh_keygen_available(),
    }


def path_info() -> dict:
    return {
        "config_dir": str(app_config_dir()),
        "data_dir": str(app_data_dir()),
        "config_file": str(config_path()),
        "database_file": str(database_path()),
    }


def permission_checks() -> list[dict]:
    checks = []
    for path in [app_config_dir(), app_data_dir(), config_path(), database_path()]:
        p = Path(path)
        exists = p.exists()
        readable = os.access(p, os.R_OK) if exists else False
        writable = os.access(p, os.W_OK) if exists else False
        mode = None
        if exists:
            mode = oct(stat.S_IMODE(p.stat().st_mode))
        checks.append({
            "path": str(p),
            "exists": exists,
            "readable": readable,
            "writable": writable,
            "mode": mode,
        })
    return checks


def dependency_checks() -> list[dict]:
    results = []
    for mod in ("flask", "rich"):
        try:
            __import__(mod)
            results.append({"module": mod, "available": True})
        except ImportError:
            results.append({"module": mod, "available": False})
    return results


def run_doctor() -> dict:
    return {
        "everlink_version": VERSION,
        "python": python_info(),
        "openssh": openssh_info(),
        "paths": path_info(),
        "permissions": permission_checks(),
        "dependencies": dependency_checks(),
    }
