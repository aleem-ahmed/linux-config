# Software check
if ! command -v vim &> /dev/null; then
	# If package manager is pacman
    if command -v pacman >/dev/null 2>&1; then
        cmd="sudo pacman -S vim"
    # If package manager is apt
    elif command -v apt >/dev/null 2>&1; then
        cmd="sudo apt install vim"
    # If package manager is dnf
    elif command -v dnf >/dev/null 2>&1; then
        cmd="sudo dnf install vim"
    else
        cmd="your distro's package manager to install python3"
    fi

    echo "[zsh] Command 'vim' not found. Please run '$cmd'"
fi

if ! command -v nvim &> /dev/null; then
	# If package manager is pacman
    if command -v pacman >/dev/null 2>&1; then
        cmd="sudo pacman -S neovim"
    # If package manager is apt
    elif command -v apt >/dev/null 2>&1; then
        cmd="sudo apt install neovim"
    # If package manager is dnf
    elif command -v dnf >/dev/null 2>&1; then
        cmd="sudo dnf install neovim"
    else
        cmd="your distro's package manager to install python3"
    fi

    echo "[zsh] Command 'nvim' not found. Please run '$cmd'"
fi

# Functions
gall() {
	git add .;
	git commit -m $1;
	git push;
}

colors()
{
	for x in {0..8}; do
		for i in {30..37}; do
			for a in {40..47}; do
				echo -ne "\e[$x;$i;$a""m\\\e[$x;$i;$a""m\e[0;37;40m "
			done
			echo
		done
	done

	echo ""
}
