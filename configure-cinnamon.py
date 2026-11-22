#!/usr/bin/env python3
"""Cinnamon desktop setup: gsettings tweaks, panel widgets, GNOME Terminal look."""

import shlex
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent

GSETTINGS = [
	("org.cinnamon", "workspace-expo-view-as-grid", "true"),
	("org.nemo.preferences", "show-hidden-files", "true"),
]

# (script, gets this script's command-line args)
SUB_SCRIPTS = [
	(SCRIPT_DIR / "cinnamon-widget" / "add_widgets_to_panel.py", False),
	(SCRIPT_DIR / "cinnamon-widget" / "set_grouped_window_list.py", False),
	(SCRIPT_DIR / "cinnamon-widget" / "set_calendar_format.py", True),
	(SCRIPT_DIR / "cinnamon-widget" / "set_workspace_switcher.py", False),
	(SCRIPT_DIR / "gnome-terminal" / "set_gnome_terminal_font.py", False),
	(SCRIPT_DIR / "gnome-terminal" / "set_gnome_terminal_theme_dracula.py", False),
	(SCRIPT_DIR / "gnome-terminal" / "set_gnome_terminal_transparency.py", False),
]

# Colors only when printing to a real terminal
_TTY = sys.stdout.isatty()
BOLD = "\033[1m" if _TTY else ""
DIM = "\033[2m" if _TTY else ""
CYAN = "\033[36m" if _TTY else ""
GREEN = "\033[32m" if _TTY else ""
RED = "\033[31m" if _TTY else ""
RESET = "\033[0m" if _TTY else ""


def step(msg):
	print(f"\n{BOLD}{CYAN}==> {msg}{RESET}", flush=True)


def ok(msg):
	print(f"  {GREEN}✓{RESET} {msg}", flush=True)


def fail(msg):
	sys.exit(f"{RED}Error:{RESET} {msg}")


def run(cmd):
	print(f"  {DIM}${RESET} {shlex.join(map(str, cmd))}", flush=True)
	result = subprocess.run(cmd)

	if result.returncode != 0:
		fail(f"command failed ({result.returncode}): {shlex.join(map(str, cmd))}")


def main():
	# Check every script up front so a missing one doesn't leave you half-configured
	missing = [script for script, _ in SUB_SCRIPTS if not script.is_file()]

	if missing:
		fail("can't find:\n" + "\n".join(f"  {script}" for script in missing))

	step("Applying gsettings")

	for schema, key, value in GSETTINGS:
		run(["gsettings", "set", schema, key, value])

	ok("gsettings applied")

	for script, pass_args in SUB_SCRIPTS:
		step(f"Running {script.relative_to(SCRIPT_DIR)}")
		# sys.executable = the same python3 running this script
		run([sys.executable, str(script), *(sys.argv[1:] if pass_args else [])])

	print(f"\n{BOLD}{GREEN}Done.{RESET}", flush=True)


if __name__ == "__main__":
	main()
