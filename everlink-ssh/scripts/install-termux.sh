#!/usr/bin/env bash
# Termux-specific helper for installing EverLink SSH dependencies.
set -euo pipefail

echo "[everlink-termux] Installing OpenSSH and Python..."
pkg update -y
pkg install -y python openssh

echo "[everlink-termux] Done. Run: bash install.sh --mode full"
