# Installation — EverLink SSH

EverLink SSH supports two installation modes through a single unified installer:

- `--mode cli` — CLI only
- `--mode gui` — GUI only
- `--mode full` — CLI + GUI (default)

Run:

```bash
bash install.sh --mode full
```

The installer is idempotent — running it again is safe.

---

## Native Termux (Android)

Termux does not provide systemd, sudo, or conventional desktop paths. The
installer detects Termux via `PREFIX` and `/data/data/com.termux`.

```bash
pkg update -y && pkg install -y python openssh
cd everlink-ssh
bash install.sh --mode full
export PATH="$HOME/.local/bin:$PATH"
```

- OpenSSH is installed with Termux's `pkg` package manager.
- Python virtualenv is created under `.venv/` in the project directory.
- The CLI launcher goes to `$HOME/.local/bin/everlink`.
- The Flask GUI runs locally through your browser at `http://127.0.0.1:5000`.
- No desktop environment or systemd is assumed.

Dedicated helper: `scripts/install-termux.sh`

---

## Ubuntu Linux (including proot-distro)

```bash
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv openssh-client
cd everlink-ssh
bash install.sh --mode full
export PATH="$HOME/.local/bin:$PATH"
```

- Checks for Python 3, pip, venv, and OpenSSH client.
- Runs under proot-distro without requiring systemd.
- Optional desktop-launcher integration is offered only when a desktop
  environment is detected (the installer itself does not create desktop files;
  add one manually if desired).

Dedicated helper: `scripts/install-ubuntu.sh`

---

## Installation modes

| Mode | What's installed |
|------|------------------|
| cli  | System deps + venv + `everlink` CLI launcher |
| gui  | System deps + venv; run `everlink gui` or `python3 run.py` |
| full | CLI launcher + GUI support (default) |

Options:

```bash
bash install.sh --mode cli        # CLI only
bash install.sh --mode gui        # GUI only
bash install.sh --mode full       # both (default)
bash install.sh --no-deps         # skip system dependency install
bash install.sh --no-venv         # skip virtualenv creation
```

---

## Uninstallation

```bash
bash uninstall.sh
```

This removes the `everlink` launcher and optionally the virtualenv. User data
(`~/.local/share/everlink-ssh`, `~/.config/everlink-ssh`) is preserved by
default. To remove it entirely, delete those directories manually.

---

## Verification

After installation:

```bash
everlink --help
everlink version
everlink doctor
everlink gui          # then open http://127.0.0.1:5000
```
