"""EverLink SSH command-line interface.

Uses argparse. All OpenSSH invocations go through ssh_manager (argument arrays,
never shell interpolation). Host-key verification is left at 'ask'.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional, Sequence

from . import __version__, APP_TITLE, __tagline__
from . import config as cfg
from . import database as db
from .security import (
    ValidationError,
    validate_hostname,
    validate_profile_name,
    validate_port,
    validate_username,
    validate_identity_file,
)
from .ssh_manager import connect, connect_raw, keygen, list_public_keys, ssh_available, tcp_reachability
from .diagnostics import run_doctor


def _confirm(prompt: str) -> bool:
    try:
        answer = input(f"{prompt} [y/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    return answer in ("y", "yes")


def cmd_add(args: argparse.Namespace) -> int:
    try:
        name = validate_profile_name(args.name)
        hostname = validate_hostname(args.host)
        username = validate_username(args.user)
        port = validate_port(args.port)
        identity_file = validate_identity_file(args.identity_file)
    except ValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    conn = db.get_connection()
    try:
        db.init_db()
        if db.get_host(conn, name) is not None:
            print(f"Error: profile '{name}' already exists.", file=sys.stderr)
            return 2
        db.add_host(conn, name, hostname, username, port, identity_file)
        print(f"Added profile '{name}' -> {username}@{hostname}:{port}")
        if identity_file:
            print(f"  identity file: {identity_file}")
        return 0
    finally:
        conn.close()


def cmd_list(args: argparse.Namespace) -> int:
    db.init_db()
    conn = db.get_connection()
    try:
        hosts = db.list_hosts(conn, search=args.search)
    finally:
        conn.close()

    if not hosts:
        print("No saved hosts. Add one with: everlink add NAME --host HOST --user USER")
        return 0

    print("Saved hosts:")
    for h in hosts:
        ident = h["identity_file"] or "(default key)"
        print(f"  {h['name']:<20} {h['username']}@{h['hostname']}:{h['port']}  [{ident}]")
    return 0


def cmd_connect(args: argparse.Namespace) -> int:
    # NAME or USER@HOST target
    target = args.target
    profile = None

    if "@" in target and not target.startswith("-"):
        # Direct connection string USER@HOST
        user, _, host = target.partition("@")
        try:
            username = validate_username(user)
            hostname = validate_hostname(host)
        except ValidationError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 2
        profile = {"username": username, "hostname": hostname, "port": args.port or 22, "identity_file": args.identity_file}
    else:
        # Saved profile
        try:
            name = validate_profile_name(target)
        except ValidationError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 2
        db.init_db()
        conn = db.get_connection()
        try:
            row = db.get_host(conn, name)
        finally:
            conn.close()
        if row is None:
            print(f"Error: no saved profile named '{name}'.", file=sys.stderr)
            print("  Add it with: everlink add NAME --host HOST --user USER")
            return 2
        profile = dict(row)

    if not ssh_available():
        print("Error: OpenSSH client ('ssh') is not installed.", file=sys.stderr)
        return 3

    target_str = f"{profile['username']}@{profile['hostname']}:{profile.get('port', 22)}"
    print(f"Connecting to {target_str} ...")
    try:
        return connect(profile)
    except KeyboardInterrupt:
        print("\nConnection cancelled.")
        return 130


def cmd_remove(args: argparse.Namespace) -> int:
    try:
        name = validate_profile_name(args.name)
    except ValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    db.init_db()
    conn = db.get_connection()
    try:
        row = db.get_host(conn, name)
        if row is None:
            print(f"Error: no saved profile named '{name}'.", file=sys.stderr)
            return 2
        print(f"Profile: {name} -> {row['username']}@{row['hostname']}:{row['port']}")
        if not args.yes and not _confirm(f"Remove profile '{name}'?"):
            print("Cancelled.")
            return 1
        db.delete_host(conn, row["id"])
        print(f"Removed profile '{name}'.")
        return 0
    finally:
        conn.close()


def cmd_test(args: argparse.Namespace) -> int:
    try:
        name = validate_profile_name(args.name)
    except ValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    db.init_db()
    conn = db.get_connection()
    try:
        row = db.get_host(conn, name)
    finally:
        conn.close()
    if row is None:
        print(f"Error: no saved profile named '{name}'.", file=sys.stderr)
        return 2

    profile = dict(row)
    target = f"{profile['username']}@{profile['hostname']}"
    port = int(profile.get("port", 22))
    print(f"Testing connection to {target}:{port} ...")

    reachable, message = tcp_reachability(profile["hostname"], port, timeout=args.timeout)
    status = "reachable" if reachable else "unreachable"
    print(f"  TCP: {message} ({status})")

    try:
        rc = connect(profile, command="exit")
        if rc == 0:
            print("  SSH: authenticated and session closed successfully.")
            db.record_attempt(conn if False else db.get_connection(), name, target, "ok", "ssh ok")
            print("Result: connection test passed.")
            return 0
        else:
            print(f"  SSH: session ended with code {rc}.")
            print("Result: connection test failed (SSH returned non-zero).")
            return 1
    except Exception as exc:  # noqa: BLE001
        print(f"  SSH: error — {exc}")
        print("Result: connection test failed.")
        return 1


def cmd_keygen(args: argparse.Namespace) -> int:
    if not ssh_available():
        print("Error: OpenSSH client ('ssh') is not installed.", file=sys.stderr)
        return 3
    path = args.path or os.path.expanduser("~/.ssh/id_ed25519")
    try:
        from .security import validate_identity_file
        path = validate_identity_file(path)
    except ValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    rc, out, err = keygen(key_type=args.type, path=path, comment=args.comment, passphrase=args.passphrase or "")
    if rc == 0:
        print(f"Key generated at {path}")
        print(out.strip())
        return 0
    else:
        print(f"ssh-keygen failed (code {rc}):", file=sys.stderr)
        print(err.strip(), file=sys.stderr)
        return 1


def cmd_keys(args: argparse.Namespace) -> int:
    keys = list_public_keys(args.ssh_dir)
    if not keys:
        print("No public keys found in ~/.ssh")
        return 0
    print("Public keys:")
    for k in keys:
        print(f"  {k['name']:<20} {k['path']}  ({k['size']} bytes)")
    return 0


def cmd_gui(args: argparse.Namespace) -> int:
    from .web import create_app
    settings = cfg.load_settings()
    host = args.host or settings.get("web_host", cfg.DEFAULT_WEB_HOST)
    port = args.port or settings.get("web_port", cfg.DEFAULT_WEB_PORT)
    print(f"Starting EverLink SSH GUI on http://{host}:{port}")
    app = create_app()
    app.run(host=host, port=port, debug=False)
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    info = run_doctor()
    print(f"EverLink SSH v{info['everlink_version']}")
    print("=" * 40)
    py = info["python"]
    print(f"Python: {py['executable']} ({py['version']})")
    ossh = info["openssh"]
    print(f"ssh: {ossh['ssh'] or 'NOT FOUND'}")
    print(f"ssh-keygen: {ossh['ssh-keygen'] or 'NOT FOUND'}")
    print(f"ssh-add: {ossh['ssh-add'] or 'NOT FOUND'}")
    print()
    print("Paths:")
    for k, v in info["paths"].items():
        print(f"  {k}: {v}")
    print()
    print("Permissions:")
    for c in info["permissions"]:
        print(f"  {c['path']}: exists={c['exists']} readable={c['readable']} writable={c['writable']} mode={c['mode']}")
    print()
    print("Dependencies:")
    for d in info["dependencies"]:
        print(f"  {d['module']}: {'ok' if d['available'] else 'MISSING'}")
    return 0


def cmd_version(args: argparse.Namespace) -> int:
    print(f"{APP_TITLE} v{__version__}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="everlink",
        description=f"{APP_TITLE} — {__tagline__}",
    )
    parser.add_argument("--version", action="store_true", help="print version and exit")

    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    def add_common(parser_obj):
        pass

    p_add = sub.add_parser("add", help="save a host profile")
    p_add.add_argument("name", help="profile name")
    p_add.add_argument("--host", required=True, help="hostname or IP address")
    p_add.add_argument("--user", required=True, help="SSH username")
    p_add.add_argument("--port", type=int, default=cfg.DEFAULT_SSH_PORT, help="SSH port (default: 22)")
    p_add.add_argument("--identity-file", dest="identity_file", default=None, help="absolute path to identity file")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="list saved host profiles")
    p_list.add_argument("--search", dest="search", default=None, help="search term")
    p_list.set_defaults(func=cmd_list)

    p_connect = sub.add_parser("connect", help="connect to a host")
    p_connect.add_argument("target", help="profile name or USER@HOST")
    p_connect.add_argument("--port", type=int, default=None, help="override port (direct connect only)")
    p_connect.add_argument("--identity-file", dest="identity_file", default=None, help="override identity file")
    p_connect.set_defaults(func=cmd_connect)

    p_remove = sub.add_parser("remove", help="remove a saved profile")
    p_remove.add_argument("name", help="profile name")
    p_remove.add_argument("--yes", action="store_true", help="skip confirmation")
    p_remove.set_defaults(func=cmd_remove)

    p_test = sub.add_parser("test", help="run a connection diagnostic")
    p_test.add_argument("name", help="profile name")
    p_test.add_argument("--timeout", type=float, default=3.0, help="TCP timeout in seconds")
    p_test.set_defaults(func=cmd_test)

    p_keygen = sub.add_parser("keygen", help="create an SSH key")
    p_keygen.add_argument("--type", default="ed25519", help="key type (default: ed25519)")
    p_keygen.add_argument("--path", default=None, help="output key path")
    p_keygen.add_argument("--comment", default="", help="key comment")
    p_keygen.add_argument("--passphrase", default="", help="key passphrase")
    p_keygen.set_defaults(func=cmd_keygen)

    p_keys = sub.add_parser("keys", help="list available public keys")
    p_keys.add_argument("--ssh-dir", default=None, help="ssh directory (default: ~/.ssh)")
    p_keys.set_defaults(func=cmd_keys)

    p_gui = sub.add_parser("gui", help="start the Flask GUI")
    p_gui.add_argument("--host", default=None, help="bind host (default: 127.0.0.1)")
    p_gui.add_argument("--port", type=int, default=None, help="bind port (default: 5000)")
    p_gui.set_defaults(func=cmd_gui)

    p_doctor = sub.add_parser("doctor", help="inspect Python, OpenSSH, permissions, dependencies")
    p_doctor.set_defaults(func=cmd_doctor)

    p_version = sub.add_parser("version", help="print installed version")
    p_version.set_defaults(func=cmd_version)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if "--version" in argv:
        print(f"{APP_TITLE} v{__version__}")
        return 0
    parser = build_parser()
    if not argv:
        parser.print_help()
        print()
        print(__tagline__)
        return 0
    args = parser.parse_args(argv)
    if getattr(args, "version", False):
        print(f"{APP_TITLE} v{__version__}")
        return 0
    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return 0
    return func(args)


if __name__ == "__main__":
    raise SystemExit(main())
