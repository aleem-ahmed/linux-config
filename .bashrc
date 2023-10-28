# [source]

# [software-checkll]
if ! command -v nvim &> /dev/null; then
        echo "[~/.bashrc] Command 'nvim' not found. Please run 'sudo apt install neovim'"
fi

# [alias]
## [python]
alias py="python3"

## [location]
alias todesktop="cd ~/Desktop"
alias todesk="cd ~/Desktop"
alias todocs="cd ~/Documents"
alias topics="cd ~/Pictures"
alias Desktop="cd ~/Desktop"
alias desktop="cd ~/Desktop"
alias desk="cd ~/Desktop"
alias downloads="cd ~/Downloads"
alias docs="cd ~/Documents"

## [yield-sync]
alias ys="cd ~/Desktop/yield-sync"
alias ysa="cd ~/Desktop/yield-sync/v1-amp"
alias ysv="cd ~/Desktop/yield-sync/v1-vaults"
alias ysv1v="cd ~/Desktop/yield-sync/v1-vaults"
alias ysfront="cd ~/Desktop/yield-sync/frontend"
alias ysf="cd ~/Desktop/yield-sync/frontend"
alias yss="cd ~/Desktop/yield-sync/specifications"

## [w3st]
alias w3st="cd ~/Desktop/w3st-io/w3st.io"
alias jjvinyls="cd ~/Desktop/w3st-io/jjvinyls"
alias toheroku="cd ~/Desktop/heroku"

## [npm]
alias nlint="npm run lint"
alias ndev="npm run dev"
alias nserve="npm run serve"
alias ninstall="npm install"

### [hardhat]
alias hh="npx hardhat"
alias hht="npx hardhat test"
alias hardhattest="npx hardhat test"
alias hardhatdeploy="npx hardhat run --network $1 scripts/deploy.js"

## [mongodb]
alias mdbstart="sudo systemctl start mongod"
alias mdbstatus="sudo systemctl status mongod"
alias mdbstop="sudo systemctl stop mongod"

## [git]
alias gadd="git add"
alias gcommit="git commit -m"
alias gpul="git pull"
alias gpush="git push"
alias gclone="git clone"
alias gco="git checkout"
alias gcom="git checkout master"
alias gstatus="git status"
alias grepb="git branch | grep $1"

## [vim]
alias vi="vi -u ~/.vimrc"

## [grep]
alias grep2="find --type f | xargs grep -e $1 -l | xargs grep -e $2 -l"

## [sql]
### Prereq. sudo apt install mysql mysql-server
alias dbstart="sudo /etc/init.d/mysql start"
alias dbstatus="sudo /etc/init.d/mysql status"
alias dbstop="sudo /etc/init.d/mysql stop"
alias dbrestart="sudo /etc/init.d/mysql restart"
alias mysql="sudo mysql --prompt='\u@\h [\d]> '"

## [general]
alias ll="ls -alF"
alias la="ls -A"
alias l="ls -CF"
alias x="exit"
alias src="source ~/.bashrc && tmux source-file ~/.tmux.conf"
alias cs="vi ~/.bashrc"
alias t="tmux -u"
# Add an "alert" alias for long running commands.
## Use like so:
## `sleep 10; alert``
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# If not running interactively, don't do anything
case $- in
	*i*) ;;
	*) return;;
esac

# don't put duplicate lines or lines starting with space in the history. See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary, update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
	debian_chroot=$(cat /etc/debian_chroot)
fi

# If this is an xterm set the title to user@host:dir
case "$TERM" in
	xterm*|rxvt*)
		PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
		;;
	*)
		;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
	test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
	alias ls='ls --color=auto'
	
	alias grep='grep --color=auto'
	alias fgrep='fgrep --color=auto'
	alias egrep='egrep --color=auto'
fi

# enable programmable completion features (you don't need to enable this, if it's already enabled in /etc/bash.bashrc
# and /etc/profile sources /etc/bash.bashrc).
if ! shopt -oq posix; then
	if [ -f /usr/shar/bash-completion/bash_completion ]; then
		. /usr/share/bash-completion/bash_completion
	elif [ -f /etc/bash_completion ]; then
		. /etc/bash_completion
	fi
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
	xterm-color|*-256color) color_prompt=yes;;
esac

if [ -n "$force_color_prompt" ]; then
	if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
		# We have color support; assume it's compliant with Ecma-48 (ISO/IEC-6429). (Lack of such support is extremely
		# rare, and such a case would tend to support setf rather than setaf.)
		color_prompt=yes
	else
		color_prompt=
	fi
fi

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

p_user="\[\033[01;31m\]\u\[\033[00m\]"
p_host="\[\033[01;32m\]\h\[\033[00m\]"
p_location="\[\033[01;34m\]\w\[\033[00m\]"
p_git_branch="\[\033[01;33m\]\$(parse_git_branch)\[\033[00m\]"

if [ "$color_prompt" = yes ]; then
	# [prompt-original]
	PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:$location\$ "
	
	# [prompt-zen]
	PS1="$p_user@$p_host $p_location $p_git_branch \n➤ "
else
	# [prompt-original]
	PS1="${debian_chroot:+($debian_chroot)}\u@\h:\w\$ "
	# [prompt-zen]
	PS1="${debian_chroot:+($debian_chroot)}\u \h \w\ "
fi

unset color_prompt force_color_prompt

# Created by `pipx` on 2022-05-24 14:00:42
export PATH="$PATH:/home/harpoon/.local/bin"

## Time Format
# %l:%M:%S %p  [%Y/%m/%d]

## SCT (Set color temperature) Application for setting redshift
. "$HOME/.cargo/env"
