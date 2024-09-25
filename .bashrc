# Load Cargo environment
. "$HOME/.cargo/env"

# History settings
HISTCONTROL=ignoreboth    # Avoid duplicates in history
shopt -s histappend       # Append to history file
shopt -s checkwinsize     # Check window size after each command

# History length
HISTSIZE=1000
HISTFILESIZE=2000

# Environment variables
export PATH="$PATH:/home/harpoon/.local/bin"

# Aliases
alias cls="clear"
alias ls="ls --group-directories-first -A"
alias ll="ls --group-directories-first -alFA"
alias la="ls -A"
alias l="ls -CF"
alias x="exit"
alias src="source ~/.bashrc && tmux source-file ~/.tmux.conf"
alias cs="vi ~/.bashrc"
alias t="tmux -u"

alias chrome="google-chrome"
alias py="python3"

# Directory navigation aliases
alias todesktop="cd ~/Desktop"
alias todocs="cd ~/Documents"
alias topics="cd ~/Pictures"
alias downloads="cd ~/Downloads"
alias desktop="cd ~/Desktop"
alias desk="desktop"

# NPM aliases
alias ndev="npm run dev"
alias ninstall="npm install"
alias nlint="npm run lint"
alias nserve="npm run serve"
alias ntest="npm run test"

# Hardhat aliases
alias hh="npx hardhat"
alias hht="npx hardhat test"
alias hardhattest="npx hardhat test"
alias hardhatdeploy="npx hardhat run --network $1 scripts/deploy.js"

# MongoDB aliases
alias mdbstart="sudo systemctl start mongod"
alias mdbstatus="sudo systemctl status mongod"
alias mdbstop="sudo systemctl stop mongod"

# Git aliases
alias gadd="git add"
alias gcommit="git commit -m"
alias gpull="git pull"
alias gpush="git push"
alias gclone="git clone"
alias gco="git checkout"
alias gcom="git checkout master"
alias gstatus="git status"
alias grepb="git branch -r | grep $1"

# Vim alias
alias vi="vi -u ~/.vimrc"

# Grep alias
alias grep2="find --type f | xargs grep -e $1 -l | xargs grep -e $2 -l"

# SQL aliases
alias installsql="sudo apt install mysql mysql-server"
alias dbstart="sudo /etc/init.d/mysql start"
alias dbstatus="sudo /etc/init.d/mysql status"
alias dbstop="sudo /etc/init.d/mysql stop"
alias sql="sudo mysql --prompt='\\u@\\h (\\d) > '"

# Project navigation aliases
YIELD_SYNC_LOCATION="~/Desktop/yield-sync"
alias ys="cd $YIELD_SYNC_LOCATION"
alias yse="cd $YIELD_SYNC_LOCATION/v1-emp"
alias ysef="cd $YIELD_SYNC_LOCATION/frontend-v1-emp"
alias ysvf="cd $YIELD_SYNC_LOCATION/frontend-v1-vaults"
alias ysv="cd $YIELD_SYNC_LOCATION/v1-vaults"
alias ysfront="cd $YIELD_SYNC_LOCATION/frontend"
alias yss="cd $YIELD_SYNC_LOCATION/specifications"
alias yssr="cd $YIELD_SYNC_LOCATION/server"
alias yssdk="cd $YIELD_SYNC_LOCATION/v1-sdk"

alias w3="cd ~/Desktop/w3st-io"
alias w3st="cd ~/Desktop/w3st-io/w3st.io"
alias jjvinyls="cd ~/Desktop/w3st-io/jjvinyls"
alias toheroku="cd ~/Desktop/heroku"

if ! command -v zsh &> /dev/null
then
	echo "[~/.bashrc] Please install zsh and oh-my-zsh using the commented out line before.."
	#sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
fi

# Software check
if ! command -v nvim &> /dev/null; then
    echo "[~/.bashrc] Command 'nvim' not found. Please run 'sudo apt install neovim'"
else
	alias vi="nvim"
fi

# If not running interactively, don't do anything
case $- in
	*i*) ;;
	*) return;;
esac

# Make less more friendly for non-text input files
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# Set variable identifying the chroot you work in
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
	debian_chroot=$(cat /etc/debian_chroot)
fi

# Set xterm title
case "$TERM" in
	xterm*|rxvt*)
		PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
		;;
	*)
		;;
esac

# Enable color support for ls and add handy aliases
if [ -x /usr/bin/dircolors ]; then
	test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
	alias ls='ls --color=auto'
	alias grep='grep --color=auto'
	alias fgrep='fgrep --color=auto'
	alias egrep='egrep --color=auto'
fi

# Enable programmable completion features
if ! shopt -oq posix; then
	if [ -f /usr/share/bash-completion/bash_completion ]; then
		. /usr/share/bash-completion/bash_completion
	elif [ -f /etc/bash_completion ]; then
		. /etc/bash_completion
	fi
fi

# Set prompt style
case "$TERM" in
	xterm-color|*-256color) color_prompt=yes;;
esac

if [ -n "$force_color_prompt" ]; then
	if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
		color_prompt=yes
	else
		color_prompt=
	fi
fi

p_user="\[\033[01;31m\]\u\[\033[00m\]"
p_host="\[\033[01;32m\]\h\[\033[00m\]"
p_location="\[\033[01;34m\]\w\[\033[00m\]"
p_git_branch="\[\033[01;33m\]\$(parse_git_branch)\[\033[00m\]"

if [ "$color_prompt" = yes ]; then
	# Prompt style options
	PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:$location\$ "
	PS1="$p_user@$p_host $p_location $p_git_branch \n➤ "
else
	PS1="${debian_chroot:+($debian_chroot)}\u \h \w "
fi

unset color_prompt force_color_prompt

# Functions
gall() {
	git add .;
	git commit -m "$1";
	git push;
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
	echo ""
}

parse_git_branch() {
	git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}

# Time format
# %l:%M:%S %p [%Y/%m/%d]
