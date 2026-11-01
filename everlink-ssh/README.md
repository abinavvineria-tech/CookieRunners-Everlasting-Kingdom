# EverLink SSH

**One Connection. Two Interfaces. Endless Possibilities.**

EverLink SSH is a secure, modern SSH connection manager with two interfaces:

- **EverLink CLI** — a terminal-based interface (`everlink`) for SSH connections,
  saved hosts, diagnostics, and configuration.
- **EverLink GUI** — a responsive Flask web application (`everlink gui`) for
  managing SSH hosts and launching connections.
- **EverLink Installer** — a unified installer supporting CLI-only, GUI-only,
  or full installation.

Target environments: Android (native Termux) and Ubuntu Linux, including Ubuntu
inside proot-distro.

> **Independent & unofficial.** This project is not affiliated with, endorsed by,
> or connected to Devsisters or the Cookie Run franchise. It is an independent
> open-source SSH client.

---

## Features

- Save, list, edit, and delete SSH host profiles (metadata only — no passwords).
- Real OpenSSH connections via safe subprocess argument arrays (no shell injection).
- Interactive terminal sessions with passphrase and host-key confirmation.
- Host-key verification left at `ask` — never silently disabled or auto-trusted.
- SSH key generation (`ssh-keygen`) and public-key listing (public info only).
- Connection diagnostics (TCP reachability + SSH session test).
- `everlink doctor` — inspect Python, OpenSSH, permissions, dependencies.
- Flask web GUI: dashboard, host manager, SSH keys, diagnostics, settings.
- Localhost-only Flask server (127.0.0.1), no debug mode, CSRF protection.
- SQLite host metadata stored in a per-user app directory (XDG/Termux aware).
- Unified installer (`install.sh`) with CLI/GUI/full modes.
- Automated test suite with `pytest`.

---

## Installation

### Quick start (Termux)

```bash
pkg update -y && pkg install -y python openssh
cd everlink-ssh
bash install.sh --mode full
export PATH="$HOME/.local/bin:$PATH"
everlink --help
everlink add myserver --host example.com --user alice --port 2222
everlink connect myserver
everlink gui
```

### Quick start (Ubuntu / proot-distro)

```bash
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv openssh-client
cd everlink-ssh
bash install.sh --mode full
export PATH="$HOME/.local/bin:$PATH"
everlink gui   # open http://127.0.0.1:5000 in your browser
```

See `INSTALLATION.md` for full details, platform-specific instructions, and the
uninstaller.

---

## CLI examples

```bash
everlink                     # show help
everlink version             # print version
everlink doctor              # system diagnostics

everlink add web --host example.com --user alice --port 2222
everlink list
everlink connect web
everlink connect alice@example.com:2222   # direct connect
everlink test web                  # TCP + SSH diagnostic
everlink remove web                # confirm before deleting
everlink keygen                    # generate an SSH key
everlink keys                      # list public keys
everlink gui                       # start Flask GUI on localhost
```

See `CLI.md` for the complete command reference.

---

## SSH keys

EverLink SSH uses OpenSSH's existing authentication mechanisms. It never reads,
displays, or transmits private-key contents.

```bash
everlink keygen --type ed25519 --comment "my key"
everlink keys
```

Add the resulting public key to your remote host's `~/.ssh/authorized_keys`.

---

## Security

- Flask bound to `127.0.0.1` by default — not exposed to the network.
- No hardcoded credentials, tokens, or private keys.
- No passwords stored in the host database.
- CSRF tokens on state-changing web routes.
- Request-size limits and secure cookie settings.
- Subprocess argument arrays — no shell interpolation.
- Host-key verification at `ask` — unknown/changed keys are never silently trusted.

See `SECURITY.md` for the full security model and limitations.

---

## Project limitations

- This is a connection manager, not a full terminal emulator. The GUI launches
  the local OpenSSH client; on devices without a usable native terminal (e.g.
  some Termux configurations), use the CLI or copy the connection command.
- No browser-based interactive terminal is implemented (deliberate — see SECURITY.md).
- Tested on Android (Termux) and Ubuntu Linux. Other distributions are
  "where practical" and not formally claimed.

---

## Uninstallation

```bash
bash everlink-ssh/uninstall.sh
```

User data (`~/.local/share/everlink-ssh`, `~/.config/everlink-ssh`) is preserved
unless you delete it manually.

---

## License

MIT License. See `LICENSE`.

---

**CookieVerse Hermes** — independent developer tooling. Every project tells a story.
Every line of code builds a kingdom. Every memory keeps the legend alive.
