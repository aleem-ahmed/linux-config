# --- Software check ---
# Prints the install command for this distro. usage: _pkg_install_cmd <pacman pkg> <apt pkg> <dnf pkg>
_pkg_install_cmd()
{
	if command -v pacman &>/dev/null; then
		echo "sudo pacman -S $1"
	elif command -v apt &>/dev/null; then
		echo "sudo apt install $2"
	elif command -v dnf &>/dev/null; then
		echo "sudo dnf install $3"
	else
		echo "your distro's package manager to install $1"
	fi
}

# Warns if a command is missing. usage: _require <command> <pacman pkg> [apt pkg] [dnf pkg]
# apt/dnf names default to the pacman name when they're the same.
_require()
{
	local bin=$1 pac=$2 apt=${3:-$2} dnf=${4:-${3:-$2}}

	if ! command -v "$bin" &>/dev/null; then
		echo "[zsh] Command '$bin' not found. Please run '$(_pkg_install_cmd "$pac" "$apt" "$dnf")'"
	fi
}

_require python3 python python3 python3
_require vim vim
_require nvim neovim
_require glow glow

# Helpers aren't needed after startup, keep them out of your shell
unfunction _require _pkg_install_cmd


# --- Functions ---
gall() {
	git add .
	git commit -m "$*"
	git push
}

colors() {
	for x in {0..8}; do
		for i in {30..37}; do
			for a in {40..47}; do
				echo -ne "\e[$x;$i;$a""m\\\e[$x;$i;$a""m\e[0;37;40m "
			done

			echo
		done
	done
}

play() {
	yt-dlp -q -f bestaudio -o - "ytsearch:$*" | mpv --no-video -
}
