#!/usr/bin/env python3
"""Enable background transparency in GNOME Terminal (Arch / AUR).

If the installed gnome-terminal lacks transparency support, offers to replace it
with the patched AUR package, then configures the default profile.
"""
import argparse
import os
import shutil
import subprocess
import sys

TRANSPARENCY_PERCENT = 15  # 0 = solid, 100 = fully see-through
PATCHED_PKG = "gnome-terminal-transparency"
REQUIRED_KEYS = {"use-transparent-background", "background-transparency-percent"}

def die(msg: str) -> None:
	print(f"Error: {msg}", file=sys.stderr)

	sys.exit(1)

def gsettings(*args: str, check: bool = True) -> subprocess.CompletedProcess:
	return subprocess.run(["gsettings", *args], capture_output=True, text=True, check=check)

def default_profile_schema() -> str:
	if not shutil.which("gsettings"):
		die("gsettings not found, can't configure GNOME Terminal.")

	res = gsettings("get", "org.gnome.Terminal.ProfilesList", "default", check=False)

	if res.returncode != 0:
		die("GNOME Terminal settings not found. Is GNOME Terminal installed?")

	uuid = res.stdout.strip().strip("'")

	# A fresh setup can have no default set; fall back to the first profile.
	if not uuid:
		res = gsettings("get", "org.gnome.Terminal.ProfilesList", "list", check=False)
		profiles = [p.strip(" '") for p in res.stdout.strip().strip("[]").split(",") if p.strip(" '")]

		if not profiles:
			die("No GNOME Terminal profiles found. Open GNOME Terminal once, then rerun.")

		uuid = profiles[0]

	return f"org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{uuid}/"

def available_keys(schema: str) -> set[str]:
	res = gsettings("list-keys", schema, check=False)

	if res.returncode != 0:
		die(f"Couldn't read profile keys:\n{res.stderr.strip()}")

	return set(res.stdout.split())

def package_installed(pkg: str) -> bool:
	if not shutil.which("pacman"):
		return False

	return subprocess.run(["pacman", "-Q", pkg], capture_output=True).returncode == 0

def confirm(prompt: str) -> bool:
	try:
		return input(f"{prompt} [y/N] ").strip().lower() in ("y", "yes")
	except EOFError:
		return False

def install_patched(assume_yes: bool) -> None:
	if not shutil.which("yay"):
		die("yay isn't installed; set it up from the AUR first.")

	if not assume_yes and not confirm(f"Install {PATCHED_PKG}? This replaces gnome-terminal."):
		die(f"Aborted. Install manually with: yay -S {PATCHED_PKG}")

	# --ask 4 auto-answers "yes" to pacman's remove-conflicting-package prompt,
	# which --noconfirm alone would answer "no".
	res = subprocess.run(["yay", "-S", "--needed", "--noconfirm", "--ask", "4", PATCHED_PKG])

	if res.returncode != 0:
		die(f"yay failed to install {PATCHED_PKG}.")

def ensure_support(schema: str, assume_yes: bool) -> set[str]:
	keys = available_keys(schema)

	if REQUIRED_KEYS <= keys:
		return keys

	print("This GNOME Terminal build doesn't support transparency.", file=sys.stderr)

	if not shutil.which("pacman"):
		die("Your distro's GNOME Terminal needs a transparency patch.")

	if package_installed(PATCHED_PKG):
		die(
			f"{PATCHED_PKG} is installed but its settings schema isn't loaded.\n"
			"Try: sudo glib-compile-schemas /usr/share/glib-2.0/schemas"
		)

	install_patched(assume_yes)

	keys = available_keys(schema)
	if not REQUIRED_KEYS <= keys:
		die(
			"Installed, but the transparency keys still aren't visible.\n"
			"Try: sudo glib-compile-schemas /usr/share/glib-2.0/schemas"
		)
	return keys

def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)

	parser.add_argument("-y", "--yes", action="store_true", help="install the patched package without asking")
	parser.add_argument(
		"-p",
		"--percent",
		type=int,
		default=TRANSPARENCY_PERCENT,
		help=f"transparency 0-100 (default {TRANSPARENCY_PERCENT})",
	)

	args = parser.parse_args()

	if not 0 <= args.percent <= 100:
		die("--percent must be between 0 and 100.")

	if os.geteuid() == 0:
		die("Don't run this as root; it configures your user's settings and yay refuses root.")

	schema = default_profile_schema()
	keys = ensure_support(schema, args.yes)

	if "use-theme-transparency" in keys:
		gsettings("set", schema, "use-theme-transparency", "false")

	gsettings("set", schema, "use-transparent-background", "true")
	gsettings("set", schema, "background-transparency-percent", str(args.percent))

	print(f"GNOME Terminal background transparency set to {args.percent}%.")
	print(
		"If you just installed the patched package, close every GNOME Terminal window "
		  "(or run: pkill gnome-terminal-server) so it restarts with the new build."
	)

if __name__ == "__main__":
	main()
