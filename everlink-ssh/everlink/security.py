"""Security helpers: input validation, CSRF tokens, and filesystem permissions.

Never trust untrusted input. All values that reach OpenSSH are passed through a
subprocess argument array, never interpolated into a shell command string.
"""

from __future__ import annotations

import os
import re
import secrets
import stat
from pathlib import Path
from typing import Optional

HOSTNAME_OR_IP_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.\-]*[A-Za-z0-9]$|^[A-Za-z0-9]$")
IPV6_RE = re.compile(r"^[0-9A-Fa-f:]+$")
PORT_RE = re.compile(r"^[0-9]+$")
PROFILE_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _.\-]{0,63}$")


class ValidationError(ValueError):
    """Raised when user-supplied input fails validation."""


def validate_port(value) -> int:
    """Validate and coerce a TCP/SSH port number."""
    try:
        port = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"Port must be an integer, got {value!r}")
    if port < 1 or port > 65535:
        raise ValidationError(f"Port must be between 1 and 65535, got {port}")
    return port


def validate_hostname(value: str) -> str:
    """Validate a hostname or IP address (IPv4 dotted or IPv6 colon form)."""
    if not value or not isinstance(value, str):
        raise ValidationError("Hostname is required")
    value = value.strip()
    if len(value) == 0:
        raise ValidationError("Hostname is required")
    if len(value) > 253:
        raise ValidationError("Hostname too long")
    if ":" in value:
        if not IPV6_RE.match(value):
            raise ValidationError(f"Invalid hostname or IP address: {value}")
    else:
        if not HOSTNAME_OR_IP_RE.match(value):
            raise ValidationError(f"Invalid hostname: {value}")
        if value.startswith("-") or value.endswith("-"):
            raise ValidationError(f"Invalid hostname: {value}")
        if value.startswith(".") or value.endswith("."):
            raise ValidationError(f"Invalid hostname: {value}")
        if ".." in value:
            raise ValidationError(f"Invalid hostname: {value}")
        # Each DNS label must not start or end with a hyphen.
        for label in value.split("."):
            if label.startswith("-") or label.endswith("-"):
                raise ValidationError(f"Invalid hostname: {value}")
    return value


def validate_profile_name(value: str) -> str:
    """Validate a saved host profile name."""
    if not value or not isinstance(value, str):
        raise ValidationError("Profile name is required")
    value = value.strip()
    if len(value) == 0:
        raise ValidationError("Profile name is required")
    if not PROFILE_NAME_RE.match(value):
        raise ValidationError(
            "Profile name must start with a letter or digit and contain only "
            "letters, digits, spaces, underscores, dots, and hyphens"
        )
    return value


def validate_identity_file(value) -> Optional[str]:
    """Validate an optional absolute identity-file path."""
    if value is None or str(value).strip() == "":
        return None
    value = str(value).strip()
    p = Path(value)
    if not p.is_absolute():
        raise ValidationError("Identity file must be an absolute path")
    return value


def validate_username(value: str) -> str:
    if not value or not isinstance(value, str):
        raise ValidationError("Username is required")
    value = value.strip()
    if len(value) == 0:
        raise ValidationError("Username is required")
    if len(value) > 64:
        raise ValidationError("Username too long")
    if not re.match(r"^[A-Za-z0-9_.\-]+$", value):
        raise ValidationError(f"Invalid username: {value}")
    return value


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def constant_time_compare(a: str, b: str) -> bool:
    return secrets.compare_digest(a or "", b or "")


def ensure_private_path(path: Path, mode: int = 0o700) -> None:
    path.mkdir(parents=True, exist_ok=True)
    try:
        path.chmod(mode)
    except OSError:
        pass


def ensure_private_file(path: Path, mode: int = 0o600) -> None:
    if path.exists():
        try:
            path.chmod(mode)
        except OSError:
            pass


def is_path_within(base: Path, target: Path) -> bool:
    """Return True if target resolves inside base (prevents path traversal)."""
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
