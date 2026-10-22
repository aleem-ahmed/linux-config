#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WINDOW_LIST_SCRIPT="$SCRIPT_DIR/set_grouped_window_list.py"
CALENDAR_SCRIPT="$SCRIPT_DIR/set_calendar_format.py"

# Ensure that python3 is installed
if ! command -v python3 >/dev/null 2>&1; then
    # If package manager is pacman
  if command -v pacman >/dev/null 2>&1; then
    cmd="sudo pacman -S python"
    # If package manager is apt
  elif command -v apt >/dev/null 2>&1; then
    cmd="sudo apt install python3"
  # If package manager is dnf
  elif command -v dnf >/dev/null 2>&1; then
    cmd="sudo dnf install python3"
  else
    cmd="your distro's package manager to install python3"
  fi

  echo "Error: Python 3 is not installed." >&2

  echo "Install it with: $cmd" >&2

  exit 1
fi

if [ -f "$CALENDAR_SCRIPT" ]; then
    python3 "$CALENDAR_SCRIPT" "$@"
else
    echo "Error: can't find $CALENDAR_SCRIPT" >&2
    exit 1
fi

if [ -f "$WINDOW_LIST_SCRIPT" ]; then
    python3 "$WINDOW_LIST_SCRIPT"
else
    echo "Error: can't find $WINDOW_LIST_SCRIPT" >&2
    exit 1
fi
