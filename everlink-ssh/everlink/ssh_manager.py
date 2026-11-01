"""Safe OpenSSH integration.

OpenSSH is always invoked through a subprocess argument array. Untrusted input
is never interpolated into a shell command string. Host-key verification is
never silently disabled.
"""

from __future__ import annotations

import os
import shutil
import socket
import subprocess
from pathlib import Path
from typing import Optional


def which(program: str) -> Optional[str]:
    return shutil.which(program)


def ssh_available() -> bool:
    return which("ssh") is not None


def ssh_keygen_available() -> bool:
    return which("ssh-keygen") is not None


def build_ssh_command(
    *,
    user: Optional[str] = None,
    host: str,
    port: int = 22,
    identity_file: Optional[str] = None,
    extra: Optional[list[str]] = None,
    command: Optional[str] = None,
) -> list[str]:
    """Build a safe argv list for OpenSSH.

    Never uses shell interpolation. StrictHostKeyChecking is left at 'ask' so
    new/changed host keys are never silently trusted.
    """
    ssh = which("ssh") or "ssh"
    args: list[str] = [ssh]
    # Interactive session: allow passphrase and host-key prompts.
    args.append("-oBatchMode=no")
    args.append("-oStrictHostKeyChecking=ask")
    if port:
        args += ["-p", str(port)]
    if identity_file:
        args += ["-i", identity_file]
    if extra:
        args += extra
    target = host
    if user:
        target = f"{user}@{host}"
    if command:
        args += [target, command]
    else:
        args.append(target)
    return args


def connect(profile: dict, command: Optional[str] = None) -> int:
    """Launch an interactive OpenSSH session bound to the real terminal.

    stdin/stdout/stderr are inherited so SSH can prompt for passphrases and
    host-key confirmation. Returns the process return code.
    """
    args = build_ssh_command(
        user=profile.get("username"),
        host=profile["hostname"],
        port=int(profile.get("port", 22)),
        identity_file=profile.get("identity_file"),
        command=command,
    )
    env = os.environ.copy()
    env.pop("SSH_ASKPASS", None)
    proc = subprocess.run(args, stdin=None, stdout=None, stderr=None, env=env)
    return proc.returncode


def connect_raw(args: list[str]) -> int:
    env = os.environ.copy()
    env.pop("SSH_ASKPASS", None)
    proc = subprocess.run(args, stdin=None, stdout=None, stderr=None, env=env)
    return proc.returncode


def keygen(
    *,
    key_type: str = "ed25519",
    path: Optional[str] = None,
    comment: str = "",
    passphrase: str = "",
) -> tuple[int, str, str]:
    """Run ssh-keygen. Returns (returncode, stdout, stderr)."""
    keygen_bin = which("ssh-keygen") or "ssh-keygen"
    out_path = path or os.path.expanduser("~/.ssh/id_ed25519")
    args = [keygen_bin, "-t", key_type, "-f", out_path, "-C", comment]
    args += ["-N", passphrase]
    proc = subprocess.run(args, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def list_public_keys(ssh_dir: Optional[str] = None) -> list[dict]:
    """List public keys in the user's .ssh directory. Public information only."""
    if ssh_dir is None:
        ssh_dir = os.path.expanduser("~/.ssh")
    p = Path(ssh_dir)
    if not p.is_dir():
        return []
    keys = []
    for file in sorted(p.iterdir()):
        if file.is_file() and file.suffix == ".pub":
            keys.append({
                "name": file.stem,
                "path": str(file),
                "size": file.stat().st_size,
            })
    return keys


def tcp_reachability(host: str, port: int = 22, timeout: float = 3.0) -> tuple[bool, str]:
    """Check TCP reachability. Distinct from successful SSH authentication."""
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True, f"Port {port} open on {host}"
    except socket.timeout:
        return False, f"Connection to {host}:{port} timed out after {timeout}s"
    except OSError as exc:
        return False, f"Cannot reach {host}:{port} — {exc}"
