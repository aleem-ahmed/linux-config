#!/usr/bin/env python3
"""Install the System Monitor applet (sysmonitor@orcus), show only RAM, and put it first on the main panel's right."""

import ast
import io
import json
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path


UUID = "sysmonitor@orcus"
SPICE_URL = f"https://cinnamon-spices.linuxmint.com/files/applets/{UUID}.zip"
APPLETS_DIR = Path.home() / ".local" / "share" / "cinnamon" / "applets"
CONFIG_DIR = Path.home() / ".config" / "cinnamon" / "spices" / UUID

# Panel zone to put the applet in; order 0 is the zone's leftmost slot
ZONE = "right"

# Only the memory graph is turned on
GRAPHS = {
	"cpu_enabled": False,
	"mem_enabled": True,
	"swap_enabled": False,
	"net_enabled": False,
	"load_enabled": False,
}


def ok(msg):
	print(f"  ✓ {msg}", flush=True)


def fail(msg):
	sys.exit(f"Error: {msg}")


def run(cmd):
	print(f"  $ {' '.join(cmd)}", flush=True)
	result = subprocess.run(cmd)

	if result.returncode != 0:
		fail(f"command failed ({result.returncode}): {' '.join(cmd)}")


def gsettings_get(key):
	result = subprocess.run(
		["gsettings", "get", "org.cinnamon", key],
		capture_output=True,
		text=True,
	)

	if result.returncode != 0:
		fail(f"gsettings get org.cinnamon {key} failed: {result.stderr.strip()}")

	# An empty string array comes back as "@as []"
	return ast.literal_eval(result.stdout.strip().removeprefix("@as "))


def has_gtop():
	# Checked in a fresh interpreter so a just-installed typelib gets picked up
	check = "import gi; gi.require_version('GTop', '2.0')"

	return subprocess.run([sys.executable, "-c", check], capture_output=True).returncode == 0


def ensure_gtop():
	if has_gtop():
		ok("libgtop already installed")
		return

	if shutil.which("apt-get"):
		run(["sudo", "apt-get", "install", "-y", "gir1.2-gtop-2.0"])
	elif shutil.which("pacman"):
		run(["sudo", "pacman", "-S", "--needed", "--noconfirm", "libgtop"])
	else:
		fail("libgtop (GTop 2.0 typelib) is missing and I don't know this package manager; install it yourself")

	if not has_gtop():
		fail("libgtop was installed but GTop 2.0 still can't be loaded")

	ok("libgtop installed")


def install_applet():
	target = APPLETS_DIR / UUID

	if (target / "metadata.json").is_file():
		ok(f"{UUID} already installed")
		return target

	print(f"  downloading {SPICE_URL}", flush=True)

	try:
		with urllib.request.urlopen(SPICE_URL, timeout=30) as response:
			data = response.read()

		with zipfile.ZipFile(io.BytesIO(data)) as archive:
			names = archive.namelist()

			# Spices zips normally hold a top-level <uuid>/ folder; handle a flat zip too
			if names and all(name.startswith(f"{UUID}/") for name in names):
				archive.extractall(APPLETS_DIR)
			else:
				archive.extractall(target)
	except (OSError, zipfile.BadZipFile) as err:
		fail(f"couldn't download or unpack {UUID}: {err}")

	if not (target / "metadata.json").is_file():
		fail(f"{UUID} unpacked but {target / 'metadata.json'} is missing")

	ok(f"{UUID} installed to {target}")

	return target


def version_key(name):
	try:
		return tuple(int(part) for part in name.split("."))
	except ValueError:
		return None


def find_schema(applet_dir):
	root = applet_dir / "settings-schema.json"

	if root.is_file():
		return root

	# Multiversion applets keep their files in folders like 3.2/; use the newest one
	versions = [
		folder
		for folder in applet_dir.iterdir()
		if folder.is_dir() and version_key(folder.name) and (folder / "settings-schema.json").is_file()
	]

	if not versions:
		fail(f"no settings-schema.json found in {applet_dir}")

	newest = max(versions, key=lambda folder: version_key(folder.name))

	return newest / "settings-schema.json"


def write_config(schema_path, instance_id):
	path = CONFIG_DIR / f"{instance_id}.json"

	if path.is_file():
		config = json.loads(path.read_text())
	else:
		# Same shape Cinnamon writes on first load: the schema with a "value" added to every setting
		config = json.loads(schema_path.read_text())

		for entry in config.values():
			if isinstance(entry, dict) and "default" in entry:
				entry["value"] = entry["default"]

	for key, value in GRAPHS.items():
		if key not in config:
			fail(f"setting {key!r} not found in {path.name}; the applet may have changed its options")

		config[key]["value"] = value

	CONFIG_DIR.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps(config, indent=4))
	ok(f"RAM-only settings written to {path}")


def main_panel():
	panels = gsettings_get("panels-enabled")

	if not panels:
		fail("no panels enabled")

	# Entries look like "1:0:bottom" (panel id : monitor : position); the first one is the main panel
	return f"panel{panels[0].split(':')[0]}"


def pick_instance_id(applets, panel):
	# Reuse the instance already on this panel so its settings file carries over
	for entry in applets:
		fields = entry.split(":")

		if len(fields) >= 5 and fields[0] == panel and fields[3] == UUID:
			return int(fields[4])

	ids = [entry.split(":")[4] for entry in applets if len(entry.split(":")) >= 5]

	return max((int(i) for i in ids if i.isdigit()), default=0) + 1


def place_first(applets, panel, instance_id):
	"""Return enabled-applets with UUID at order 0 in ZONE of `panel`, the rest of that zone renumbered after it."""
	others = []
	zone = []

	for entry in applets:
		fields = entry.split(":")

		if len(fields) < 5 or fields[0] != panel:
			others.append(entry)
		elif fields[3] == UUID:
			continue
		elif fields[1] == ZONE:
			zone.append(fields)
		else:
			others.append(entry)

	zone.sort(key=lambda fields: int(fields[2]) if fields[2].isdigit() else 0)
	renumbered = [":".join([fields[0], fields[1], str(order), *fields[3:]]) for order, fields in enumerate(zone, 1)]

	return [f"{panel}:{ZONE}:0:{UUID}:{instance_id}", *renumbered, *others]


def main():
	ensure_gtop()
	applet_dir = install_applet()
	schema = find_schema(applet_dir)

	panel = main_panel()
	applets = gsettings_get("enabled-applets")
	instance_id = pick_instance_id(applets, panel)

	# Settings go in before the applet is enabled, so it starts up already showing only RAM
	write_config(schema, instance_id)

	new_applets = place_first(applets, panel, instance_id)

	run(["gsettings", "set", "org.cinnamon", "enabled-applets", str(new_applets)])
	ok(f"{UUID} is first on the {ZONE} side of {panel}")


if __name__ == "__main__":
	main()
