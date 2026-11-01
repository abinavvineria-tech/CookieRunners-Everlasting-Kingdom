"""EverLink SSH configuration and path management.

All user data lives in a per-user application directory. XDG conventions are
respected where practical; Termux and proot-distro Ubuntu both work with the
fallback paths below.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

APP_NAME = "everlink-ssh"
APP_TITLE = "EverLink SSH"
VERSION = "1.0.0"

DEFAULT_SSH_PORT = 22
DEFAULT_WEB_HOST = "127.0.0.1"
DEFAULT_WEB_PORT = 5000

CONFIG_FILE_NAME = "settings.json"
DATABASE_FILE_NAME = "everlink.db"


def is_termux() -> bool:
    prefix = os.environ.get("PREFIX", "")
    return "com.termux" in prefix or os.path.exists("/data/data/com.termux")


def _env_dir(key: str) -> Path | None:
    value = os.environ.get(key)
    if value:
        return Path(value).expanduser().resolve()
    return None


def app_data_dir() -> Path:
    """Per-user application data directory (XDG_DATA_HOME where set)."""
    override = _env_dir("EVERLINK_APP_DIR")
    if override:
        return override
    xdg = os.environ.get("XDG_DATA_HOME")
    if xdg:
        return Path(xdg) / APP_NAME
    return Path.home() / ".local" / "share" / APP_NAME


def app_config_dir() -> Path:
    """Per-user application config directory (XDG_CONFIG_HOME where set)."""
    override = _env_dir("EVERLINK_APP_DIR")
    if override:
        return override
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / APP_NAME
    return Path.home() / ".config" / APP_NAME


def database_path() -> Path:
    return app_data_dir() / DATABASE_FILE_NAME


def config_path() -> Path:
    return app_config_dir() / CONFIG_FILE_NAME


DEFAULT_SETTINGS = {
    "default_ssh_port": DEFAULT_SSH_PORT,
    "web_host": DEFAULT_WEB_HOST,
    "web_port": DEFAULT_WEB_PORT,
    "theme": "midnight",
    "terminal_preference": "native",
}


def load_settings() -> dict:
    settings = dict(DEFAULT_SETTINGS)
    path = config_path()
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as f:
                user = json.load(f)
            if isinstance(user, dict):
                settings.update(user)
        except (OSError, json.JSONDecodeError):
            # Corrupt settings file: keep defaults, do not crash.
            pass
    return settings


def save_settings(settings: dict) -> None:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.parent.chmod(0o700)
    except OSError:
        pass
    with path.open("w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
    try:
        path.chmod(0o600)
    except OSError:
        pass
