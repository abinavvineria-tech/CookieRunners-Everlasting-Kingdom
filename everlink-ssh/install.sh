#!/usr/bin/env bash
# EverLink SSH — installer
# Supports CLI-only, GUI-only, or full installation on Termux and Ubuntu Linux.
set -euo pipefail

APP_NAME="everlink-ssh"
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$APP_DIR/.venv"
MODE="full"

log()  { printf '\033[1;36m[everlink-install]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[warn]\033[0m %s\n' "$*"; }
err()  { printf '\033[1;31m[error]\033[0m %s\n' "$*" >&2; }

usage() {
  cat <<EOF
Usage: $0 [--mode cli|gui|full] [--no-deps] [--no-venv]

Install EverLink SSH.

Options:
  --mode MODE     Installation mode: cli, gui, or full (default: full)
  --no-deps       Skip dependency installation
  --no-venv       Skip virtualenv creation
  -h, --help      Show this help

Examples:
  $0 --mode full      # CLI + GUI (default)
  $0 --mode cli       # CLI only
  $0 --mode gui       # GUI only

This installer is idempotent: running it again is safe.
EOF
}

DEPS=true
VENV=true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode) MODE="${2:-full}"; shift 2 ;;
    --no-deps) DEPS=false; shift ;;
    --no-venv) VENV=false; shift ;;
    -h|--help) usage; exit 0 ;;
    *) err "Unknown option: $1"; usage; exit 2 ;;
  esac
done

case "$MODE" in
  cli|gui|full) ;;
  *) err "Invalid mode: $MODE (use cli, gui, or full)"; exit 2 ;;
esac

detect_platform() {
  local prefix="${PREFIX:-}"
  if [[ "$prefix" == *com.termux* ]] || [[ -d /data/data/com.termux ]]; then
    echo "termux"
  elif command -v apt-get >/dev/null 2>&1; then
    echo "ubuntu"
  else
    echo "linux"
  fi
}

PLATFORM="$(detect_platform)"
log "Detected platform: $PLATFORM"
log "Installation mode: $MODE"

install_deps() {
  if [[ "$DEPS" == "false" ]]; then
    log "Skipping dependency installation (--no-deps)."
    return 0
  fi
  log "Installing system dependencies..."
  case "$PLATFORM" in
    termux)
      if command -v pkg >/dev/null 2>&1; then
        pkg update -y && pkg install -y python openssh
      else
        warn "pkg not found; assuming dependencies already present."
      fi
      ;;
    ubuntu|linux)
      if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update -y && sudo apt-get install -y python3 python3-pip python3-venv openssh-client
      else
        warn "apt-get not found; install python3, pip, venv, openssh-client manually."
      fi
      ;;
  esac
}

setup_venv() {
  if [[ "$VENV" == "false" ]]; then
    log "Skipping virtualenv creation (--no-venv)."
    return 0
  fi
  log "Creating virtual environment at $VENV_DIR..."
  if [[ ! -x "$VENV_DIR/bin/python" ]]; then
    python3 -m venv "$VENV_DIR"
  fi
  . "$VENV_DIR/bin/activate"
  log "Installing Python dependencies from requirements.txt..."
  pip install --upgrade pip >/dev/null 2>&1 || true
  pip install -r "$APP_DIR/requirements.txt"
}

install_deps
setup_venv

INSTALL_BIN="${INSTALL_BIN:-$HOME/.local/bin}"
if [[ "$MODE" == "cli" || "$MODE" == "full" ]]; then
  log "Installing 'everlink' CLI launcher..."
  mkdir -p "$INSTALL_BIN"
  cat > "$INSTALL_BIN/everlink" <<LAUNCHER
#!/usr/bin/env bash
VENV="$VENV_DIR"
if [[ -x "\$VENV/bin/python" ]]; then
  exec "\$VENV/bin/python" "$APP_DIR/run.py" "\$@"
else
  exec python3 "$APP_DIR/run.py" "\$@"
fi
LAUNCHER
  chmod +x "$INSTALL_BIN/everlink"
  log "CLI launcher installed to $INSTALL_BIN/everlink"
  log "Add $INSTALL_BIN to your PATH: export PATH=\"$INSTALL_BIN:\$PATH\""
fi

if [[ "$MODE" == "gui" || "$MODE" == "full" ]]; then
  log "GUI mode selected. Start the GUI with: everlink gui"
  log "Or: python3 $APP_DIR/run.py"
fi

log "Installation complete ($MODE)."
log "Uninstall: bash $APP_DIR/uninstall.sh"
