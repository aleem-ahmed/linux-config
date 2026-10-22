#!/usr/bin/env python3
import json
import shutil
import sys
from pathlib import Path

FORMAT = sys.argv[1] if len(sys.argv) > 1 else "%Y %b %e %I:%M:%S %p"
CONFIG_DIR = Path.home() / ".config/cinnamon/spices/calendar@cinnamon.org"

files = sorted(CONFIG_DIR.glob("*.json"))
if not files:
    sys.exit(f"No calendar configs found in {CONFIG_DIR}")

for path in files:
    shutil.copy2(path, path.with_suffix(".json.bak"))
    data = json.loads(path.read_text())

    data.setdefault("use-custom-format", {})["value"] = True
    data.setdefault("custom-format", {})["value"] = FORMAT

    path.write_text(json.dumps(data, indent=4))
    print(f"Updated {path}")

print("Done. Restart Cinnamon (Alt+F2, then r) if changes don't appear.")
