import shutil
import subprocess
import sys

TRANSPARENCY_PERCENT = 15  # 0 = solid, 100 = fully see-through
PATCHED_PKG = "gnome-terminal-transparency"


def default_profile_schema() -> str:
    if not shutil.which("gsettings"):
        sys.exit("gsettings not found, can't configure GNOME Terminal.")

    res = subprocess.run(
        ["gsettings", "get", "org.gnome.Terminal.ProfilesList", "default"],
        capture_output=True,
        text=True,
    )

    if res.returncode != 0:
        sys.exit("GNOME Terminal settings not found. Is GNOME Terminal installed?")

    uuid = res.stdout.strip().strip("'")

    return ("org.gnome.Terminal.Legacy.Profile:" f"/org/gnome/terminal/legacy/profiles:/:{uuid}/")


def available_keys(schema: str) -> set[str]:
    res = subprocess.run(
    	["gsettings", "list-keys", schema],
        capture_output=True,
        text=True,
        check=True
    )
    return set(res.stdout.split())


def package_installed(pkg: str) -> bool:
    if not shutil.which("pacman"):
        return False

    res = subprocess.run(["pacman", "-Q", pkg], capture_output=True, text=True)

    return res.returncode == 0


def explain_missing_support() -> None:
    print("Error: this GNOME Terminal build doesn't support transparency.", file=sys.stderr)

    if not shutil.which("pacman"):
        print("Your distro's GNOME Terminal needs a transparency patch.", file=sys.stderr)
        sys.exit(1)

    if package_installed(PATCHED_PKG):
        print(f"{PATCHED_PKG} is installed, but the keys are missing.", file=sys.stderr)
        print("Close all GNOME Terminal windows or log out and back in, then rerun.", file=sys.stderr)
    else:
        print(f"Install the patched version with: yay -S {PATCHED_PKG}", file=sys.stderr)

        if not shutil.which("yay"):
            print("(yay isn't installed either; set it up from the AUR first.)", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    schema = default_profile_schema()
    keys = available_keys(schema)

    required = {"use-transparent-background", "background-transparency-percent"}

    if not required <= keys:
        explain_missing_support()

    if "use-theme-transparency" in keys:
        subprocess.run(["gsettings", "set", schema, "use-theme-transparency", "false"], check=True)

    subprocess.run(["gsettings", "set", schema, "use-transparent-background", "true"], check=True)

    subprocess.run(
        ["gsettings", "set", schema, "background-transparency-percent",
        str(TRANSPARENCY_PERCENT)],
        check=True
    )

    print(f"GNOME Terminal background transparency set to {TRANSPARENCY_PERCENT}%.")
