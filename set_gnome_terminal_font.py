import io
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

FONT_NAME = "0xProto Nerd Font Mono"
FONT_SIZE = 11
URL = "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/0xProto.tar.xz"
FONT_DIR = Path.home() / ".local/share/fonts/0xProto"


def font_installed() -> bool:
    out = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True).stdout
    return FONT_NAME in out


def install_font() -> None:
    print(f"Downloading {FONT_NAME}...")
    with urllib.request.urlopen(URL) as resp:
        data = resp.read()
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:xz") as tar:
        for member in tar.getmembers():
            if "NerdFontMono" in member.name and member.name.endswith(".ttf"):
                member.name = Path(member.name).name
                tar.extract(member, FONT_DIR)
    subprocess.run(["fc-cache", "-f"], check=True)
    print(f"Installed to {FONT_DIR}")


def set_gnome_terminal_font() -> None:
    if not shutil.which("gsettings"):
        print("gsettings not found, skipping GNOME Terminal setup.")
        return
    res = subprocess.run(
        ["gsettings", "get", "org.gnome.Terminal.ProfilesList", "default"],
        capture_output=True, text=True,
    )
    if res.returncode != 0:
        print("GNOME Terminal settings not found, skipping.")
        return
    uuid = res.stdout.strip().strip("'")
    schema = ("org.gnome.Terminal.Legacy.Profile:"
              f"/org/gnome/terminal/legacy/profiles:/:{uuid}/")
    subprocess.run(["gsettings", "set", schema, "use-system-font", "false"], check=True)
    subprocess.run(["gsettings", "set", schema, "font", f"{FONT_NAME} {FONT_SIZE}"], check=True)
    print(f"GNOME Terminal now uses {FONT_NAME} {FONT_SIZE}")


if __name__ == "__main__":
    if font_installed():
        print(f"{FONT_NAME} already installed.")
    else:
        try:
            install_font()
        except Exception as e:
            sys.exit(f"Font install failed: {e}")
    set_gnome_terminal_font()
