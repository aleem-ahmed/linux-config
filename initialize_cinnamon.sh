#!/usr/bin/env bash
set -euo pipefail

gsettings set org.cinnamon workspace-expo-view-as-grid true

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

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

SET_GNOME_TERMINAL_FONT="$SCRIPT_DIR/set_gnome_terminal_font.py"

if [ -f "$SET_GNOME_TERMINAL_FONT" ]; then
    python3 "$SET_GNOME_TERMINAL_FONT"
else
    echo "Error: can't find $SET_GNOME_TERMINAL_FONT" >&2
    exit 1
fi
SET_GNOME_TERMINAL_THEME_DRACULA="$SCRIPT_DIR/set_gnome_terminal_theme_dracula.py"

if [ -f "$SET_GNOME_TERMINAL_THEME_DRACULA" ]; then
    python3 "$SET_GNOME_TERMINAL_THEME_DRACULA"
else
    echo "Error: can't find $SET_GNOME_TERMINAL_THEME_DRACULA" >&2
    exit 1
fi

SET_GNOME_TERMINAL_TRANSPARENCY="$SCRIPT_DIR/set_gnome_terminal_transparency.py"

if [ -f "$SET_GNOME_TERMINAL_TRANSPARENCY" ]; then
    python3 "$SET_GNOME_TERMINAL_TRANSPARENCY"
else
    echo "Error: can't find $SET_GNOME_TERMINAL_TRANSPARENCY" >&2
    exit 1
fi

CALENDAR_SCRIPT="$SCRIPT_DIR/set_calendar_format.py"

if [ -f "$CALENDAR_SCRIPT" ]; then
    python3 "$CALENDAR_SCRIPT" "$@"
else
    echo "Error: can't find $CALENDAR_SCRIPT" >&2
    exit 1
fi

WINDOW_LIST_SCRIPT="$SCRIPT_DIR/set_grouped_window_list.py"

if [ -f "$WINDOW_LIST_SCRIPT" ]; then
    python3 "$WINDOW_LIST_SCRIPT"
else
    echo "Error: can't find $WINDOW_LIST_SCRIPT" >&2
    exit 1
fi
