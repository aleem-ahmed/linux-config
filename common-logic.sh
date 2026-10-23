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
