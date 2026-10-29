#!/usr/bin/env python3
"""Put a Cinnamon workspace switcher first on the right side of every panel, displayed as simple buttons."""

import argparse
import json
import sys
import time
from pathlib import Path

from gi.repository import Gio


SCHEMA = "org.cinnamon"
DEFAULT_UUID = "workspace-switcher@cinnamon.org"
ZONE = "right"
DISPLAY_TYPES = ("buttons", "visual")
BACKUP_DIR = Path.home() / ".config" / "cinnamon-applet-backups"
CONFIG_ROOTS = (
	Path.home() / ".config" / "cinnamon" / "spices",
	Path.home() / ".cinnamon" / "configs",
)
CONFIG_WAIT_SECONDS = 15


def parse_args():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"--uuid",
		default=DEFAULT_UUID,
		help=f"applet UUID to add (default: {DEFAULT_UUID})",
	)
	parser.add_argument(
		"--display-type",
		choices=DISPLAY_TYPES,
		default="buttons",
		help="display style for every switcher instance (default: buttons)",
	)
	parser.add_argument("--dry-run", action="store_true", help="show what would change without writing anything")

	return parser.parse_args()


def get_panel_ids(settings):
	# Entries look like "1:0:bottom" -> panel id, monitor, position
	panel_ids = []

	for entry in settings.get_strv("panels-enabled"):
		parts = entry.split(":")

		if parts and parts[0].isdigit():
			panel_ids.append(int(parts[0]))

	return panel_ids


def parse_applet(entry):
	# Entries look like "panel1:right:3:sound@cinnamon.org:12"
	parts = entry.split(":")

	if len(parts) < 5 or not parts[0].startswith("panel"):
		return None

	try:
		return {
			"panel": int(parts[0][len("panel"):]),
			"zone": parts[1],
			"order": int(parts[2]),
			"uuid": parts[3],
			"instance": int(parts[4]),
			"extra": parts[5:],
		}
	except ValueError:
		return None


def format_applet(applet):
	parts = [
		f"panel{applet['panel']}",
		applet["zone"],
		str(applet["order"]),
		applet["uuid"],
		str(applet["instance"]),
		*applet["extra"],
	]

	return ":".join(parts)


def backup(applets):
	BACKUP_DIR.mkdir(parents=True, exist_ok=True)
	path = BACKUP_DIR / f"enabled-applets-{time.strftime('%Y%m%d-%H%M%S')}.txt"
	path.write_text("\n".join(applets) + "\n")

	return path


def arrange_applets(uuid, panel_ids, entries):
	"""Return the new entry list and the switcher instance ids, with one switcher first on each panel's right side."""
	applets = [parse_applet(e) for e in entries]
	valid = [a for a in applets if a]
	next_instance = max((a["instance"] for a in valid), default=0) + 1
	added = []
	switcher_instances = []

	for panel_id in panel_ids:
		on_panel = [a for a in valid if a["panel"] == panel_id]
		switcher = next((a for a in on_panel if a["uuid"] == uuid), None)

		if switcher is None:
			switcher = {
				"panel": panel_id,
				"zone": ZONE,
				"order": 0,
				"uuid": uuid,
				"instance": next_instance,
				"extra": [],
			}
			added.append(switcher)
			next_instance += 1
			print(f"panel{panel_id}: adding switcher (instance {switcher['instance']})")
		else:
			print(f"panel{panel_id}: moving existing switcher (instance {switcher['instance']})")

		switcher["zone"] = ZONE
		others = sorted(
			(a for a in on_panel if a["zone"] == ZONE and a is not switcher),
			key=lambda a: a["order"],
		)

		# Renumber the right zone so the switcher sits at 0 and everything else keeps its relative order
		switcher["order"] = 0

		for order, applet in enumerate(others, start=1):
			applet["order"] = order

		switcher_instances.append(switcher["instance"])

	new_entries = [format_applet(a) if a else e for a, e in zip(applets, entries)]
	new_entries.extend(format_applet(a) for a in added)

	return new_entries, switcher_instances


def find_config(uuid, instance):
	for root in CONFIG_ROOTS:
		path = root / uuid / f"{instance}.json"

		if path.exists():
			return path

	return None


def wait_for_configs(uuid, instances):
	# Cinnamon writes a new applet's config file shortly after it loads the applet
	deadline = time.monotonic() + CONFIG_WAIT_SECONDS
	found = {}

	while True:
		for instance in instances:
			if instance not in found:
				path = find_config(uuid, instance)

				if path:
					found[instance] = path

		if len(found) == len(instances) or time.monotonic() >= deadline:
			break

		time.sleep(0.5)

	return found


def set_display_type(path, display_type):
	data = json.loads(path.read_text())
	setting = data.get("display-type")

	if not isinstance(setting, dict):
		print(f"  {path.name}: no display-type setting found, skipping (older Cinnamon?)")
		return False

	if setting.get("value") == display_type:
		print(f"  {path.name}: already {display_type}")
		return False

	setting["value"] = display_type
	path.write_text(json.dumps(data, indent=4) + "\n")
	print(f"  {path.name}: set to {display_type}")

	return True


def main():
	args = parse_args()
	settings = Gio.Settings.new(SCHEMA)
	panel_ids = get_panel_ids(settings)

	if not panel_ids:
		print("No enabled panels found.", file=sys.stderr)
		return 1

	entries = list(settings.get_strv("enabled-applets"))
	new_entries, instances = arrange_applets(args.uuid, panel_ids, entries)

	if args.dry_run:
		print("Dry run. New applet list would be:")

		for entry in new_entries:
			print(f"  {entry}")

		print(f"Would set instances {instances} to {args.display_type}. No changes written.")
		return 0

	if new_entries != entries:
		backup_path = backup(entries)
		settings.set_strv("enabled-applets", new_entries)
		Gio.Settings.sync()
		print(f"Previous applet list backed up to {backup_path}")
	else:
		print("Panel layout already correct.")

	print(f"Setting display type to {args.display_type}...")
	configs = wait_for_configs(args.uuid, instances)

	for instance in instances:
		if instance not in configs:
			print(f"  {instance}.json: config file never appeared, rerun the script in a few seconds")
			continue

		set_display_type(configs[instance], args.display_type)

	print("Done.")

	return 0


if __name__ == "__main__":
	sys.exit(main())
