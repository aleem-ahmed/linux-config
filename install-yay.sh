#!/usr/bin/env bash
# install-yay.sh — installs the yay AUR helper on Arch Linux
# Usage: ./install-yay.sh          (builds yay from source)
#        ./install-yay.sh --bin    (uses prebuilt yay-bin, much faster)

set -euo pipefail

PKG="yay"
[[ "${1:-}" == "--bin" ]] && PKG="yay-bin"

info()  { printf '\e[1;34m::\e[0m %s\n' "$*"; }
error() { printf '\e[1;31mError:\e[0m %s\n' "$*" >&2; exit 1; }

# makepkg refuses to run as root
[[ $EUID -eq 0 ]] && error "Don't run this as root. Run as a normal user with sudo access."

command -v pacman >/dev/null 2>&1 || error "pacman not found — this script is for Arch-based systems."

if command -v yay >/dev/null 2>&1; then
    info "yay is already installed: $(yay --version | head -n1)"
    exit 0
fi

command -v sudo >/dev/null 2>&1 || error "sudo not found. Install it as root first: pacman -S sudo"

info "Checking requirements..."
REQUIRED=(git base-devel)
MISSING=()
for pkg in "${REQUIRED[@]}"; do
    if pacman -Qi "$pkg" >/dev/null 2>&1; then
        printf '   \e[1;32m✓\e[0m %s\n' "$pkg"
    else
        printf '   \e[1;31m✗\e[0m %s\n' "$pkg"
        MISSING+=("$pkg")
    fi
done

if (( ${#MISSING[@]} > 0 )); then
    info "Installing missing requirements: ${MISSING[*]}"
    sudo pacman -S --needed --noconfirm "${MISSING[@]}"
else
    info "All requirements already installed."
fi

BUILD_DIR="$(mktemp -d)"
trap 'rm -rf "$BUILD_DIR"' EXIT

info "Cloning $PKG from the AUR..."
git clone --depth 1 "https://aur.archlinux.org/${PKG}.git" "$BUILD_DIR/$PKG"

info "Building and installing $PKG..."
cd "$BUILD_DIR/$PKG"
makepkg -si --noconfirm

if command -v yay >/dev/null 2>&1; then
    info "Done! $(yay --version | head -n1)"
    info "Tip: run 'yay -Y --gendb' once to set up devel package tracking."
else
    error "Install finished but yay isn't on PATH — something went wrong."
fi
