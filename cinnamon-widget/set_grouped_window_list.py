#!/usr/bin/env python3
"""Ungroup apps and show window titles on every grouped window list, waiting for new applets' configs to appear."""

import json
import shutil
import time
from pathlib import Path

from gi.repository import Gio # type: ignore


UUID = "grouped-window-list@cinnamon.org"
CONFIG_DIR = Path.home() / ".config/cinnamon/spices" / UUID
TITLE_DISPLAY_WINDOW_TITLE = 3  # 1=None, 2=App name, 3=Window title, 4=Focused only
WAIT_SECONDS = 15


def get_instances():
	# Entries look like "panel1:left:3:grouped-window-list@cinnamon.org:12"
	instances = []

	for entry in Gio.Settings.new("org.cinnamon").get_strv("enabled-applets"):
		parts = entry.split(":")

		if len(parts) >= 5 and parts[3] == UUID and parts[4].isdigit():
			instances.append(int(parts[4]))

	return instances


def wait_for_configs(instances):
	deadline = time.monotonic() + WAIT_SECONDS
	paths = {i: CONFIG_DIR / f"{i}.json" for i in instances}

	while not all(p.exists() for p in paths.values()) and time.monotonic() < deadline:
		time.sleep(0.5)

	return paths


def main():
	instances = get_instances()

	if not instances:
		print("No grouped window lists on any panel, nothing to do")
		return

	for instance, path in wait_for_configs(instances).items():
		if not path.exists():
			print(f"{path.name}: config never appeared, rerun in a few seconds")
			continue

		shutil.copy2(path, path.with_suffix(".json.bak"))
		data = json.loads(path.read_text())
		data.setdefault("group-apps", {})["value"] = False
		data.setdefault("title-display", {})["value"] = TITLE_DISPLAY_WINDOW_TITLE
		path.write_text(json.dumps(data, indent=4))
		print(f"Updated {path}")

	print("Done. Restart Cinnamon (Alt+F2, then r) if changes don't appear.")


if __name__ == "__main__":
	main()
