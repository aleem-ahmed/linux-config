# Software check
if ! command -v nvim &> /dev/null; then
    echo "[zsh] Command 'nvim' not found. Please run 'sudo apt install neovim'"
else
	alias vi="nvim"
fi

# Functions
gall() {
	git add .;
	git commit -m $1;
	git push;
}

colors() {
    echo "Colors!"
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
