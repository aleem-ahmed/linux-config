#!/usr/bin/env python3
import json
import shutil
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / ".config/cinnamon/spices/grouped-window-list@cinnamon.org"
TITLE_DISPLAY_WINDOW_TITLE = 3  # 1=None, 2=App name, 3=Window title, 4=Focused only

files = sorted(CONFIG_DIR.glob("*.json"))
if not files:
    sys.exit(f"No grouped window list configs found in {CONFIG_DIR}")

for path in files:
    shutil.copy2(path, path.with_suffix(".json.bak"))
    data = json.loads(path.read_text())

    data.setdefault("group-apps", {})["value"] = False
    data.setdefault("title-display", {})["value"] = TITLE_DISPLAY_WINDOW_TITLE

    path.write_text(json.dumps(data, indent=4))
    print(f"Updated {path}")

print("Done. Restart Cinnamon (Alt+F2, then r) if changes don't appear.")
