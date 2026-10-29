"""Put exactly one grouped window list last on the left side of every Cinnamon panel."""

import time
from pathlib import Path

from gi.repository import Gio


SCHEMA = "org.cinnamon"
WINDOW_LIST_UUID = "grouped-window-list@cinnamon.org"
ZONE = "left"
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
			keep = {
				"panel": panel_id,
				"zone": ZONE,
				"order": 0,
				"uuid": WINDOW_LIST_UUID,
				"instance": next_instance,
				"extra": [],
			}
			added.append(keep)
			next_instance += 1
			print(f"panel{panel_id}: adding window list (instance {keep['instance']})")

		others = sorted(
			(a for a in on_panel if a["zone"] == ZONE and a["uuid"] != WINDOW_LIST_UUID),
			key=lambda a: a["order"],
		)

		# Renumber the left zone so everything keeps its relative order and the window list comes last
		for order, applet in enumerate(others):
			applet["order"] = order

		keep["zone"] = ZONE
		keep["order"] = len(others)

	new_entries = []

	for applet, entry in zip(applets, entries):
		if applet is None:
			new_entries.append(entry)
		elif id(applet) not in removed:
			new_entries.append(format_applet(applet))

	new_entries.extend(format_applet(a) for a in added)

	return new_entries


def update_window_lists():
	settings = Gio.Settings.new(SCHEMA)
	panel_ids = get_panel_ids(settings)

	if not panel_ids:
		print("No enabled panels found, skipping window lists")
		return

	entries = list(settings.get_strv("enabled-applets"))
	new_entries = arrange_window_lists(panel_ids, entries)

	if new_entries == entries:
		print("Window lists already in place")
		return

	BACKUP_DIR.mkdir(parents=True, exist_ok=True)
	backup_path = BACKUP_DIR / f"enabled-applets-{time.strftime('%Y%m%d-%H%M%S')}.txt"
	backup_path.write_text("\n".join(entries) + "\n")
	settings.set_strv("enabled-applets", new_entries)
	Gio.Settings.sync()
	print(f"Previous applet list backed up to {backup_path}")


def main():
	update_window_lists()
	print("Done. Restart Cinnamon (Alt+F2, then r) if changes don't appear.")


if __name__ == "__main__":
	main()
