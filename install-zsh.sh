if [ -f "$ZSH/oh-my-zsh.sh" ]; then
	source "$ZSH/oh-my-zsh.sh"
else
	echo "[~/.zshrc] '.oh-my-zsh' is not installed."
	echo -n "Do you want to install Oh My Zsh? (y/n) "
	read choice

	if [[ "$choice" =~ ^[Yy]$ ]]; then
		echo "Installing Oh My Zsh..."
		KEEP_ZSHRC=yes sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
	else
		echo "Skipping installation."
	fi
fi