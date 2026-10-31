#!/usr/bin/env python3
"""Arch Linux setup: pacman candy, yay, Mint themes, LightDM + slick-greeter. Safe to re-run."""

import difflib
import os
import shlex
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PACMAN_CONF = Path("/etc/pacman.conf")
LIGHTDM_CONF = Path("/etc/lightdm/lightdm.conf")
LIGHTDM_CONF_D = Path("/etc/lightdm/lightdm.conf.d")
SLICK_CONF = Path("/etc/lightdm/slick-greeter.conf")
XGREETERS = Path("/usr/share/xgreeters")
DM_LINK = Path("/etc/systemd/system/display-manager.service")
GREETER_PKG = "lightdm-slick-greeter"
# Session names slick-greeter has shipped under, in order of preference
GREETER_NAMES = ("lightdm-slick-greeter", "slick-greeter")

WALLPAPER = "/usr/share/backgrounds/linuxmint-wilma/aksenapati_snow_mountain.jpg"

# Colors only when printing to a real terminal
_TTY = sys.stdout.isatty()
BOLD = "\033[1m" if _TTY else ""
DIM = "\033[2m" if _TTY else ""
CYAN = "\033[36m" if _TTY else ""
GREEN = "\033[32m" if _TTY else ""
RED = "\033[31m" if _TTY else ""
YELLOW = "\033[33m" if _TTY else ""
RESET = "\033[0m" if _TTY else ""


# --- Output ---


def step(msg):
	print(f"\n{BOLD}{CYAN}==> {msg}{RESET}", flush=True)


def log(msg):
	print(f"  -> {msg}", flush=True)


def ok(msg):
	print(f"  {GREEN}✓{RESET} {msg}", flush=True)


def warn(msg):
	print(f"  {YELLOW}WARNING:{RESET} {msg}", file=sys.stderr, flush=True)


def show_cmd(cmd, note=""):
	suffix = f"  {DIM}# {note}{RESET}" if note else ""
	print(f"  {DIM}${RESET} {shlex.join(map(str, cmd))}{suffix}", flush=True)


def show_diff(path, old, new):
	diff = difflib.unified_diff(
		(old or "").splitlines(),
		new.splitlines(),
		fromfile=f"{path} (before)",
		tofile=f"{path} (after)",
		lineterm="",
	)

	for line in diff:
		color = GREEN if line.startswith("+") else RED if line.startswith("-") else DIM
		print(f"    {color}{line}{RESET}", flush=True)


# --- Helpers ---


def run(cmd, check=True, input=None, quiet=False, note=""):
	show_cmd(cmd, note)
	result = subprocess.run(
		cmd,
		check=False,
		input=input,
		text=True,
		stdout=subprocess.DEVNULL if quiet else None,
	)

	if result.returncode != 0:
		log(f"{RED}exit code {result.returncode}{RESET}")

		if check:
			raise subprocess.CalledProcessError(result.returncode, cmd)

	return result


def is_installed(pkg):
	result = subprocess.run(
		["pacman", "-Qq", pkg],
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL,
	)
	installed = result.returncode == 0
	log(f"package {pkg}: {'installed' if installed else 'not installed'}")

	return installed


def read_text(path):
	try:
		text = path.read_text()
	except FileNotFoundError:
		log(f"reading {path}: doesn't exist")

		return None
	except PermissionError:
		log(f"reading {path}: permission denied")

		return None

	log(f"reading {path}: {len(text.splitlines())} lines")

	return text


def write_root_file(path, old, new):
	log(f"changes to {path}:")
	show_diff(path, old, new)
	run(["sudo", "tee", str(path)], input=new, quiet=True, note="new content via stdin")
	ok(f"wrote {path}")


def backup_once(path):
	backup = path.with_name(path.name + ".bak")

	if not path.exists():
		log(f"no existing {path} to back up")

		return

	if backup.exists():
		log(f"backup {backup} already exists, keeping the original backup")

		return

	run(["sudo", "cp", str(path), str(backup)], note="one-time backup")
	ok(f"backed up to {backup}")


# --- Pure text transforms (no side effects, easy to test) ---


def add_ilovecandy(text):
	"""Return pacman.conf text with ILoveCandy under [options], unchanged if already there."""
	lines = text.splitlines()

	if any(line.startswith("ILoveCandy") for line in lines):
		return text

	for i, line in enumerate(lines):
		if line.strip() == "[options]":
			lines.insert(i + 1, "ILoveCandy")

			return "\n".join(lines) + "\n"

	return text


def set_greeter_session(text, greeter):
	"""Return lightdm.conf text with exactly one active greeter-session line in [Seat:*]."""
	wanted = f"greeter-session={greeter}"
	lines = text.splitlines()
	header = next((i for i, line in enumerate(lines) if line.strip() == "[Seat:*]"), None)

	if header is None:
		return text.rstrip("\n") + f"\n\n[Seat:*]\n{wanted}\n"

	end = next((i for i in range(header + 1, len(lines)) if lines[i].startswith("[")), len(lines))
	section = lines[header + 1:end]
	active = [line for line in section if line.startswith("greeter-session=")]

	if active == [wanted]:
		return text

	# Drop every greeter-session line (commented or not), then add exactly one under the header
	section = [line for line in section if not line.lstrip("#").startswith("greeter-session=")]
	lines[header + 1:end] = [wanted, *section]

	return "\n".join(lines) + "\n"


def build_slick_conf():
	theme_dir = Path("/usr/share/themes/Mint-Y-Dark")
	icons_dir = Path("/usr/share/icons/Mint-Y")
	theme = "Mint-Y-Dark" if theme_dir.is_dir() else "Adwaita-dark"
	icons = "Mint-Y" if icons_dir.is_dir() else "Adwaita"
	log(f"theme: {theme} ({'found' if theme_dir.is_dir() else f'{theme_dir} missing, using fallback'})")
	log(f"icons: {icons} ({'found' if icons_dir.is_dir() else f'{icons_dir} missing, using fallback'})")
	lines = [
		"[Greeter]",
		f"theme-name={theme}",
		f"icon-theme-name={icons}",
		"draw-user-backgrounds=false",
		"draw-grid=false",
		"show-clock=true",
		"clock-format=%a %b %-d  %-I:%M %p",
	]

	if WALLPAPER and Path(WALLPAPER).is_file():
		log(f"wallpaper: {WALLPAPER} (found)")
		lines.append(f"background={WALLPAPER}")
	elif WALLPAPER:
		warn(f"Wallpaper {WALLPAPER} not found, skipping background (greeter will be black).")
	else:
		log("wallpaper: none set (greeter will be black)")

	return "\n".join(lines) + "\n", theme, icons


# --- Checks ---


def find_greeter_session():
	"""Return the greeter-session name LightDM can actually launch, or None if slick-greeter isn't there."""
	for name in GREETER_NAMES:
		path = XGREETERS / f"{name}.desktop"

		if path.is_file():
			log(f"checking {path}: found")

			return name

		log(f"checking {path}: not found")

	# Unknown naming: take any slick desktop file rather than guessing
	log(f"searching {XGREETERS} for any *slick*.desktop")
	matches = sorted(XGREETERS.glob("*slick*.desktop")) if XGREETERS.is_dir() else []

	if matches:
		log(f"found {matches[0]}")

	return matches[0].stem if matches else None


def warn_on_dropin_overrides(greeter):
	"""Files in lightdm.conf.d override lightdm.conf; flag any that set a different greeter."""
	if not LIGHTDM_CONF_D.is_dir():
		log(f"{LIGHTDM_CONF_D} doesn't exist, no overrides to check")

		return

	files = sorted(LIGHTDM_CONF_D.glob("*.conf"))
	log(f"checking {len(files)} override file(s) in {LIGHTDM_CONF_D}")

	for path in files:
		for line in (read_text(path) or "").splitlines():
			line = line.strip()

			if line.startswith("greeter-session=") and line != f"greeter-session={greeter}":
				warn(f"{path} sets '{line}', which overrides lightdm.conf. Fix or remove that line.")


# --- Steps ---


def enable_ilovecandy():
	step("Enabling ILoveCandy in pacman.conf")
	old = PACMAN_CONF.read_text()
	log(f"reading {PACMAN_CONF}: {len(old.splitlines())} lines")
	new = add_ilovecandy(old)

	if new == old:
		ok("ILoveCandy already enabled (or no [options] section), nothing to do")

		return

	write_root_file(PACMAN_CONF, old, new)


def install_yay():
	step("Checking for yay")

	if is_installed("yay") or is_installed("yay-bin"):
		ok("yay already installed, skipping")

		return

	log(f"running {SCRIPT_DIR / 'install-yay.sh'}")
	run([str(SCRIPT_DIR / "install-yay.sh")])
	ok("yay installed")


def missing_packages(groups):
	"""Each group is a tuple of interchangeable packages; the first one is what gets installed if none are present."""
	missing = []

	for group in groups:
		present = next((pkg for pkg in group if is_installed(pkg)), None)

		if present:
			ok(f"{present} already installed")
		else:
			missing.append(group[0])

	return missing


def install_mint_themes():
	step("Installing Mint themes and icons")
	run(["sudo", "pacman", "-S", "--needed", "--noconfirm", "cinnamon"], note="--needed skips if up to date")

	# mint-themes and mint-themes-git conflict, so accept either. Skip yay entirely when nothing is missing:
	# --needed can't tell if a -git package is current, so it rebuilds them every run.
	missing = missing_packages([
		("mint-themes", "mint-themes-git"),
		("mint-y-icons", "mint-y-icons-git"),
		("mint-x-icons", "mint-x-icons-git"),
	])

	if missing:
		log(f"missing: {' '.join(missing)}")
		run(["yay", "-S", "--needed", "--noconfirm", *missing])
	else:
		ok("all Mint themes and icons already installed, skipping yay")

	missing = missing_packages([("mint-l-theme",), ("mint-l-icons",)])

	if not missing:
		return

	# Mint-L: the AUR tarballs are currently 404ing upstream; don't let it kill the script
	result = run(["yay", "-S", "--needed", "--noconfirm", *missing], check=False, note="allowed to fail")

	if result.returncode != 0:
		warn("Mint-L failed to build (upstream source 404), skipping.")
	else:
		ok("Mint-L installed")


def switch_display_manager():
	step("Setting LightDM as the display manager")
	current = DM_LINK.resolve().stem if DM_LINK.is_symlink() else ""
	log(f"{DM_LINK} -> {DM_LINK.resolve() if current else 'not set'}")

	if current == "lightdm":
		ok("LightDM is already the display manager, nothing to do")

		return

	# Takes effect on reboot; the current session is left alone (no --now)
	if current:
		log(f"current display manager: {current}, disabling it")
		run(["sudo", "systemctl", "disable", current])

	run(["sudo", "systemctl", "enable", "lightdm"], note="takes effect on reboot")
	ok("LightDM enabled")


def setup_greeter():
	step("Checking LightDM + slick-greeter packages")
	missing = [pkg for pkg in ("lightdm", GREETER_PKG, "lightdm-settings") if not is_installed(pkg)]

	if missing:
		log(f"missing: {' '.join(missing)}")
		run(["yay", "-S", "--needed", "--noconfirm", *missing], check=False)
	else:
		ok("all greeter packages already installed")

	if not (is_installed("lightdm") and is_installed(GREETER_PKG)):
		warn("LightDM/slick-greeter not installed, skipping greeter setup.")

		return

	# Bail before touching any config or the display manager, so a bad name can't leave you at a black screen
	step("Finding the slick-greeter session name")
	greeter = find_greeter_session()

	if greeter is None:
		warn(f"No slick-greeter .desktop file in {XGREETERS}; leaving your login screen as it is.")

		return

	ok(f"greeter session: {greeter}")

	step(f"Configuring {LIGHTDM_CONF}")
	old = read_text(LIGHTDM_CONF) or ""
	new = set_greeter_session(old, greeter)

	if new == old:
		ok(f"greeter-session already set to {greeter}, nothing to do")
	else:
		write_root_file(LIGHTDM_CONF, old, new)

	warn_on_dropin_overrides(greeter)

	step(f"Configuring {SLICK_CONF}")
	content, theme, icons = build_slick_conf()
	current = read_text(SLICK_CONF)

	if current == content:
		ok("slick-greeter.conf already up to date, nothing to do")
	else:
		backup_once(SLICK_CONF)
		write_root_file(SLICK_CONF, current, content)

	switch_display_manager()


def main():
	if os.geteuid() == 0:
		sys.exit("Run this as your normal user, not root (yay refuses root). It'll use sudo when needed.")

	print(f"{BOLD}Initializing Arch Linux..{RESET}", flush=True)
	step("Getting sudo")
	run(["sudo", "-v"], note="asks for your password once up front")

	try:
		enable_ilovecandy()
		install_yay()
		install_mint_themes()
		setup_greeter()
	except subprocess.CalledProcessError as e:
		sys.exit(f"\n{RED}ERROR:{RESET} command failed ({e.returncode}): {shlex.join(map(str, e.cmd))}")

	print(f"\n{BOLD}{GREEN}Done.{RESET} Reboot to see the new login screen.", flush=True)


if __name__ == "__main__":
	main()
