if command -v zsh >/dev/null 2>&1; then
	echo "[~/.bashrc] Please use zsh instead of bash."
else
	# Prompt the user (default is Yes)
	read -p "[~/.bashrc] zsh is not installed. Do you want to isntall it? (Y/n): " choice
	choice=${choice:-Y}  # Default to "Y" if the user presses Enter

	case "$choice" in
		y|Y|"" ) 
			echo "Installing zsh.."
			
			# Detect package manager and install zsh
			if command -v apt >/dev/null 2>&1; then
				sudo apt update && sudo apt install -y zsh
			elif command -v dnf >/dev/null 2>&1; then
				sudo dnf install -y zsh
			elif command -v pacman >/dev/null 2>&1; then
				sudo pacman -Sy --noconfirm zsh
			elif command -v brew >/dev/null 2>&1; then
				brew install zsh
			else
				echo "Error: No supported package manager found."
				exit 1
			fi

			echo "zsh installation complete."

			# Offer to change the default shell (default is Yes)
			read -p "Would you like to make zsh your default shell? (Y/n): " change_shell
			change_shell=${change_shell:-Y}  # Default to "Y" if the user presses Enter

			if [[ "$change_shell" =~ ^[Yy]$ || -z "$change_shell" ]]; then
				chsh -s "$(command -v zsh)"
				echo "Default shell changed to zsh. Please log out and log back in for changes to take effect."
			fi
			;;
		* )
			echo "Skipping zsh installation."
			;;
	esac
fi