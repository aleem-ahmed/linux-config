echo "Initializing Arch Linux.."

echo "Installing yay.."

./install-yay.sh

# --- Linux Mint themes (Cinnamon) ---
echo "==> Installing Mint themes and icons..."
sudo pacman -S --needed --noconfirm cinnamon

yay -S --needed --noconfirm \
    mint-themes-git \
    mint-y-icons-git \
    mint-x-icons

# Mint-L: the AUR tarballs are currently 404ing upstream; don't let it kill the script
yay -S --needed --noconfirm mint-l-theme mint-l-icons \
    || echo "WARNING: Mint-L failed to build (upstream source 404), skipping." >&2
