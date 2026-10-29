#!/usr/bin/env python3
"""Set every Cinnamon workspace switcher to simple buttons, waiting for new applets' configs to appear."""

import argparse
import json
import time
from pathlib import Path

from gi.repository import Gio # type: ignore


UUID = "workspace-switcher@cinnamon.org"
DISPLAY_TYPES = ("buttons", "visual")
CONFIG_ROOTS = (
	Path.home() / ".config" / "cinnamon" / "spices",
	Path.home() / ".cinnamon" / "configs",
)
CONFIG_WAIT_SECONDS = 15


def parse_args():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"--display-type",
		choices=DISPLAY_TYPES,
		default="buttons",
		help="display style for every switcher instance (default: buttons)",
	)

	return parser.parse_args()


def get_instances():
	# Entries look like "panel1:right:0:workspace-switcher@cinnamon.org:12"
	instances = []

	for entry in Gio.Settings.new("org.cinnamon").get_strv("enabled-applets"):
		parts = entry.split(":")

		if len(parts) >= 5 and parts[3] == UUID and parts[4].isdigit():
			instances.append(int(parts[4]))

	return instances


def find_config(instance):
	for root in CONFIG_ROOTS:
		path = root / UUID / f"{instance}.json"

		if path.exists():
			return path

	return None


def wait_for_configs(instances):
	# Cinnamon writes a new applet's config file shortly after it loads the applet
	deadline = time.monotonic() + CONFIG_WAIT_SECONDS
	found = {}

	while True:
		for instance in instances:
			if instance not in found:
				path = find_config(instance)

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
		print(f"{path.name}: no display-type setting found, skipping (older Cinnamon?)")
		return

	if setting.get("value") == display_type:
		print(f"{path.name}: already {display_type}")
		return

	setting["value"] = display_type
	path.write_text(json.dumps(data, indent=4) + "\n")
	print(f"{path.name}: set to {display_type}")


def main():
	args = parse_args()
	instances = get_instances()

	if not instances:
		print("No workspace switchers on any panel, nothing to do")
		return

	configs = wait_for_configs(instances)

	for instance in instances:
		if instance not in configs:
			print(f"{instance}.json: config file never appeared, rerun in a few seconds")
			continue

		set_display_type(configs[instance], args.display_type)

	print("Done.")


if __name__ == "__main__":
	main()
