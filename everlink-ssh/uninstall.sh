#!/usr/bin/env bash
# EverLink SSH — uninstaller
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_BIN="${INSTALL_BIN:-$HOME/.local/bin}"

log() { printf '\033[1;36m[everlink-uninstall]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[warn]\033[0m %s\n' "$*"; }

echo "This will remove the EverLink SSH CLI launcher."
echo "Application data (in ~/.local/share/everlink-ssh and ~/.config/everlink-ssh) is NOT removed by default."
echo ""
read -rp "Remove the 'everlink' launcher from $INSTALL_BIN? [y/N]: " ans
if [[ "$ans" == [yY] || "$ans" == [yY][eE][sS] ]]; then
  if [[ -f "$INSTALL_BIN/everlink" ]]; then
    rm -f "$INSTALL_BIN/everlink"
    log "Removed $INSTALL_BIN/everlink"
  else
    warn "$INSTALL_BIN/everlink not found."
  fi
else
  log "Launcher kept."
fi

read -rp "Also remove the virtualenv at $APP_DIR/.venv? [y/N]: " ans
if [[ "$ans" == [yY] || "$ans" == [yY][eE][sS] ]]; then
  rm -rf "$APP_DIR/.venv"
  log "Removed virtualenv."
fi

log "Uninstall complete."
log "To fully remove user data, delete manually: ~/.local/share/everlink-ssh ~/.config/everlink-ssh"
