#!/usr/bin/env bash
set -euo pipefail

SYSTEMD_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"

mkdir -p "$SYSTEMD_USER_DIR"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/systemd"

cp "$SCRIPT_DIR/sway-session.target" "$SYSTEMD_USER_DIR/"
cp "$SCRIPT_DIR/eww.service" "$SYSTEMD_USER_DIR/"
cp "$SCRIPT_DIR/eww-open@.service" "$SYSTEMD_USER_DIR/"

echo "Installed systemd user services to $SYSTEMD_USER_DIR"
echo "Run the following to enable and start them:"
echo "  systemctl --user daemon-reload"
echo "  systemctl --user enable --now eww.service"
