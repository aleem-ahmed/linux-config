#!/usr/bin/env python3
"""Lay out every Cinnamon panel: one grouped window list last on the left, a workspace switcher first on the right."""

import time
from pathlib import Path

from gi.repository import Gio


SCHEMA = "org.cinnamon"
WINDOW_LIST_UUID = "grouped-window-list@cinnamon.org"
WORKSPACE_SWITCHER_UUID = "workspace-switcher@cinnamon.org"
BACKUP_DIR = Path.home() / ".config" / "cinnamon-applet-backups"


def get_panel_ids(settings):
	# Entries look like "1:0:bottom" -> panel id, monitor, position
	panel_ids = []

	for entry in settings.get_strv("panels-enabled"):
		parts = entry.split(":")

		if parts and parts[0].isdigit():
			panel_ids.append(int(parts[0]))

	return panel_ids


def parse_applet(entry):
	# Entries look like "panel1:left:3:grouped-window-list@cinnamon.org:12"
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


def new_applet(panel_id, zone, uuid, instance):
	return {
		"panel": panel_id,
		"zone": zone,
		"order": 0,
		"uuid": uuid,
		"instance": instance,
		"extra": [],
	}


def rebuild_entries(applets, entries, removed, added):
	new_entries = []

	for applet, entry in zip(applets, entries):
		if applet is None:
			new_entries.append(entry)
		elif id(applet) not in removed:
			new_entries.append(format_applet(applet))

	new_entries.extend(format_applet(a) for a in added)

	return new_entries


def arrange_window_lists(panel_ids, entries):
	"""Return a new applet list with exactly one grouped window list last in each panel's left zone."""
	applets = [parse_applet(e) for e in entries]
	valid = [a for a in applets if a]
	next_instance = max((a["instance"] for a in valid), default=0) + 1
	removed = set()
	added = []

	for panel_id in panel_ids:
		on_panel = [a for a in valid if a["panel"] == panel_id]
		lists = [a for a in on_panel if a["uuid"] == WINDOW_LIST_UUID]

		if lists:
			keep = lists[0]

			for extra in lists[1:]:
				removed.add(id(extra))
				print(f"panel{panel_id}: removing duplicate window list (instance {extra['instance']})")

			print(f"panel{panel_id}: moving window list (instance {keep['instance']})")
		else:
			keep = new_applet(panel_id, "left", WINDOW_LIST_UUID, next_instance)
			added.append(keep)
			next_instance += 1
			print(f"panel{panel_id}: adding window list (instance {keep['instance']})")

		others = sorted(
			(a for a in on_panel if a["zone"] == "left" and a["uuid"] != WINDOW_LIST_UUID),
			key=lambda a: a["order"],
		)

		# Renumber the left zone so everything keeps its relative order and the window list comes last
		for order, applet in enumerate(others):
			applet["order"] = order

		keep["zone"] = "left"
		keep["order"] = len(others)

	return rebuild_entries(applets, entries, removed, added)


def arrange_workspace_switchers(panel_ids, entries):
	"""Return a new applet list with a workspace switcher first in each panel's right zone."""
	applets = [parse_applet(e) for e in entries]
	valid = [a for a in applets if a]
	next_instance = max((a["instance"] for a in valid), default=0) + 1
	added = []

	for panel_id in panel_ids:
		on_panel = [a for a in valid if a["panel"] == panel_id]
		switcher = next((a for a in on_panel if a["uuid"] == WORKSPACE_SWITCHER_UUID), None)

		if switcher is None:
			switcher = new_applet(panel_id, "right", WORKSPACE_SWITCHER_UUID, next_instance)
			added.append(switcher)
			next_instance += 1
			print(f"panel{panel_id}: adding workspace switcher (instance {switcher['instance']})")
		else:
			print(f"panel{panel_id}: moving workspace switcher (instance {switcher['instance']})")

		others = sorted(
			(a for a in on_panel if a["zone"] == "right" and a is not switcher),
			key=lambda a: a["order"],
		)

		# Renumber the right zone so the switcher sits at 0 and everything else keeps its relative order
		switcher["zone"] = "right"
		switcher["order"] = 0

		for order, applet in enumerate(others, start=1):
			applet["order"] = order

	return rebuild_entries(applets, entries, set(), added)


def update_panels():
	settings = Gio.Settings.new(SCHEMA)
	panel_ids = get_panel_ids(settings)

	if not panel_ids:
		print("No enabled panels found, skipping panel layout")
		return

	entries = list(settings.get_strv("enabled-applets"))
	new_entries = arrange_window_lists(panel_ids, entries)
	new_entries = arrange_workspace_switchers(panel_ids, new_entries)

	if new_entries == entries:
		print("Panel layout already in place")
		return

	BACKUP_DIR.mkdir(parents=True, exist_ok=True)
	backup_path = BACKUP_DIR / f"enabled-applets-{time.strftime('%Y%m%d-%H%M%S')}.txt"
	backup_path.write_text("\n".join(entries) + "\n")
	settings.set_strv("enabled-applets", new_entries)
	Gio.Settings.sync()
	print(f"Previous applet list backed up to {backup_path}")


def main():
	update_panels()
	print("Done. Restart Cinnamon (Alt+F2, then r) if changes don't appear.")


if __name__ == "__main__":
	main()
