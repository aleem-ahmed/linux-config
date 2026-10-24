echo "Initializing Arch Linux.."

echo "Installing yay.."

./install-yay.sh

# --- Linux Mint themes (Cinnamon) ---
echo "==> Installing Mint themes and icons..."
sudo pacman -S --needed --noconfirm cinnamon mint-themes mint-y-icons mint-x-icons

if command -v yay >/dev/null 2>&1; then
    yay -S --needed --noconfirm mint-l-theme mint-l-icons
else
    echo "WARNING: yay not found, skipping Mint-L theme (AUR)." >&2
fi
