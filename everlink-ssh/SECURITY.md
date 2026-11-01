# Security — EverLink SSH

Security is a core feature of EverLink SSH. This document describes the security
model, guarantees, and limitations.

---

## Network exposure

- The Flask development server binds to `127.0.0.1` by default.
- The web application is **not** exposed to the network by default.
- Flask debug mode is **never** enabled in a normal installation.
- Remote network access requires authentication and HTTPS (not yet implemented;
  do not expose the GUI to the network).

---

## Credentials and secrets

- No credentials, tokens, or private keys are hardcoded.
- **No SSH passwords are stored** in the host database.
- Only non-secret profile metadata, timestamps, and limited diagnostic history
  are stored in SQLite.
- Private-key contents are never read, displayed, or transmitted by the
  application.
- Passwords, private-key data, and authentication secrets are never logged.

---

## OpenSSH integration

- OpenSSH is invoked through a **subprocess argument array** — never shell
  interpolation. This prevents command injection.
- Host-key verification is left at `ask` (`StrictHostKeyChecking=ask`).
- New or changed host keys are **never** silently trusted or accepted.
- `UserKnownHostsFile` is not pointed at `/dev/null` (that would disable
  host-key checking).
- `SSH_ASKPASS` is removed from the environment during interactive connections
  to avoid hijacking passphrase prompts.
- Interactive sessions inherit stdin/stdout/stderr so SSH can prompt for
  passphrases and host-key confirmation in the terminal.

---

## Input validation

- Hostnames are validated (DNS label rules, no leading/trailing hyphens or
  dots, no consecutive dots).
- Ports are restricted to 1–65535.
- Profile names and usernames are validated against safe character sets.
- Identity files must be absolute paths.
- Path-traversal checks are applied where file paths are resolved.

---

## Web security

- State-changing routes are protected with **CSRF tokens** (per-session).
- Request size is limited to 1 MB.
- Session cookies are `HttpOnly` and `SameSite=Lax`.
- No unrestricted command execution is exposed through Flask routes.

---

## Filesystem

- Application data lives in a per-user directory (`~/.local/share/everlink-ssh`
  or `~/.config/everlink-ssh`, XDG-respecting, Termux-aware).
- Directories and files are created with restrictive permissions (`0o700` /
  `0o600`) where the filesystem supports it.
- Existing user SSH configuration, private keys, and host-key databases are
  **never** overwritten.
- No destructive cleanup commands are used.

---

## GUI-to-CLI connection architecture

A browser cannot directly open a native SSH terminal. EverLink SSH implements two
modes:

1. **Launch native SSH** — the local Flask backend starts OpenSSH in a local
   terminal where the environment supports it. On Termux, terminal limitations
   are documented and a reliable CLI fallback is provided.
2. **Copy connection command** — a safely generated command is shown for the
   user to copy into their terminal.

No browser-based interactive terminal is implemented (deliberate — see below).

---

## What EverLink SSH does NOT do

- Does not implement a browser-based interactive terminal (no WebSocket
  architecture, no authenticated terminal streaming). Treat this as an optional
  future feature requiring a careful security model.
- Does not store or manage SSH passwords.
- Does not disable or bypass host-key verification.
- Does not expose the web UI to the network by default.

---

## Threat model summary

| Threat | Mitigation |
|--------|------------|
| Command injection | Subprocess argument arrays, no shell interpolation |
| Credential theft | No passwords stored; private keys never read |
| Host-key spoofing | Verification at `ask`; unknown keys not trusted |
| CSRF on state changes | Per-session CSRF tokens |
| Network exposure | Localhost-only bind; no debug mode |
| Path traversal | Input validation + path containment checks |
