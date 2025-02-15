if [ -f "$ZSH/oh-my-zsh.sh" ]; then
	source "$ZSH/oh-my-zsh.sh"
else
	echo -n "[~/.zshrc] '.oh-my-zsh' is not installed. Do you want to install Oh My Zsh? (Y/n) "
	
	# Default to 'y' if Enter is pressed (empty input)
    read choice
    choice=${choice:-y}  # Default to 'y' if the user presses Enter

	if [[ "$choice" =~ ^[Yy]$ ]]; then
		echo "Installing Oh My Zsh..."
		KEEP_ZSHRC=yes sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
	else
		echo "Skipping installation."
	fi
fi