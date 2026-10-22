#!/usr/bin/env python3
import shutil
import subprocess
import sys

BACKGROUND = "#282A36"
FOREGROUND = "#F8F8F2"
SELECTION = "#44475A"
PALETTE = [
    "#21222C", "#FF5555", "#50FA7B", "#F1FA8C",  # black, red, green, yellow
    "#BD93F9", "#FF79C6", "#8BE9FD", "#F8F8F2",  # blue, magenta, cyan, white
    "#6272A4", "#FF6E6E", "#69FF94", "#FFFFA5",  # bright versions
    "#D6ACFF", "#FF92DF", "#A4FFFF", "#FFFFFF",
]


def default_profile_schema() -> str:
    if not shutil.which("gsettings"):
        sys.exit("gsettings not found, can't configure GNOME Terminal.")
    res = subprocess.run(
        ["gsettings", "get", "org.gnome.Terminal.ProfilesList", "default"],
        capture_output=True, text=True,
    )
    if res.returncode != 0:
        sys.exit("GNOME Terminal settings not found. Is GNOME Terminal installed?")
    uuid = res.stdout.strip().strip("'")
    return ("org.gnome.Terminal.Legacy.Profile:"
            f"/org/gnome/terminal/legacy/profiles:/:{uuid}/")


def gset(schema: str, key: str, value: str) -> None:
    subprocess.run(["gsettings", "set", schema, key, value], check=True)


if __name__ == "__main__":
    schema = default_profile_schema()
    palette = "[" + ", ".join(f"'{c}'" for c in PALETTE) + "]"

    gset(schema, "use-theme-colors", "false")
    gset(schema, "background-color", BACKGROUND)
    gset(schema, "foreground-color", FOREGROUND)
    gset(schema, "palette", palette)
    gset(schema, "bold-color-same-as-fg", "true")
    gset(schema, "cursor-colors-set", "true")
    gset(schema, "cursor-background-color", FOREGROUND)
    gset(schema, "cursor-foreground-color", BACKGROUND)
    gset(schema, "highlight-colors-set", "true")
    gset(schema, "highlight-background-color", SELECTION)
    gset(schema, "highlight-foreground-color", FOREGROUND)

    print("GNOME Terminal is now using Dracula.")
