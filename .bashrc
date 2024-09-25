# Load Cargo environment
. "$HOME/.cargo/env"

# History settings
HISTCONTROL=ignoreboth    # Avoid duplicates in history
shopt -s histappend       # Append to history file
shopt -s checkwinsize     # Check window size after each command

# History length
HISTSIZE=1000
HISTFILESIZE=2000

source ./exports.sh
source ./aliases.sh
source ./common-logic.sh

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
