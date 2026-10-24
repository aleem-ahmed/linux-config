#!/usr/bin/env python3
"""Enable background transparency in GNOME Terminal.

On Arch, installs the patched AUR package if the current build lacks support.
"""
import argparse
import os
import shutil
import subprocess
import sys
from typing import NoReturn

PATCHED_PKG = "gnome-terminal-transparency"
REQUIRED_KEYS = {"use-transparent-background", "background-transparency-percent"}
SCHEMA_HINT = "Try: sudo glib-compile-schemas /usr/share/glib-2.0/schemas"


def die(msg: str) -> NoReturn:
	sys.exit(f"Error: {msg}")


def gsettings(*args: str) -> str:
	res = subprocess.run(["gsettings", *args], capture_output=True, text=True)
	if res.returncode != 0:
		die(res.stderr.strip() or f"gsettings {' '.join(args)} failed")

	return res.stdout.strip()


def profile_schema() -> str:
	uuid = gsettings("get", "org.gnome.Terminal.ProfilesList", "default").strip("'")

	if not uuid:
		profiles = gsettings("get", "org.gnome.Terminal.ProfilesList", "list")
		uuid = profiles.strip("[]").split(",")[0].strip(" '")

	if not uuid:
		die("No GNOME Terminal profiles found. Open GNOME Terminal once, then rerun.")

	return f"org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{uuid}/"


def keys(schema: str) -> set[str]:
	return set(gsettings("list-keys", schema).split())


def install_patched(assume_yes: bool) -> None:
	if not shutil.which("yay"):
		die("No transparency support, and yay isn't available to install the patched build.")

	if not assume_yes:
		answer = input(f"Install {PATCHED_PKG}? This replaces gnome-terminal. [y/N] ")

		if answer.strip().lower() not in ("y", "yes"):
			die(f"Aborted. Install manually with: yay -S {PATCHED_PKG}")

	# --ask 4 auto-accepts pacman's remove-conflicting-package prompt.
	cmd = ["yay", "-S", "--needed", "--noconfirm", "--ask", "4", PATCHED_PKG]

	if subprocess.run(cmd).returncode != 0:
		die(f"yay failed to install {PATCHED_PKG}.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)

	parser.add_argument(
		"-y", "--yes",
		action="store_true",
		help="install the patched package without asking",
	)

	parser.add_argument(
		"-p", "--percent",
		type=int,
		default=15,
		choices=range(101),
		metavar="0-100",
		help="transparency percent (default 15)",
	)

	args = parser.parse_args()

	if os.geteuid() == 0:
		die("Don't run this as root; it configures your user's settings.")

	if not shutil.which("gsettings"):
		die("gsettings not found.")

	schema = profile_schema()
	available = keys(schema)

	if not REQUIRED_KEYS <= available:
		install_patched(args.yes)
		available = keys(schema)

		if not REQUIRED_KEYS <= available:
			die(f"Transparency keys still missing. {SCHEMA_HINT}")

	if "use-theme-transparency" in available:
		gsettings("set", schema, "use-theme-transparency", "false")

	gsettings("set", schema, "use-transparent-background", "true")
	gsettings("set", schema, "background-transparency-percent", str(args.percent))

	print(
		f"Transparency set to {args.percent}%. "
		"If the package was just installed, run: pkill gnome-terminal-server"
	)

if __name__ == "__main__":
	main()
