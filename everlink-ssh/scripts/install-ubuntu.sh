#!/usr/bin/env bash
# Ubuntu-specific helper for installing EverLink SSH dependencies.
set -euo pipefail

echo "[everlink-ubuntu] Installing Python, pip, venv, OpenSSH..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv openssh-client

echo "[everlink-ubuntu] Done. Run: bash install.sh --mode full"
