# Aliases
alias cls="clear"
alias ls="ls --group-directories-first -A --color='auto'"
alias ll="ls --group-directories-first -alFA --color='auto'"
alias la="ls -A"
alias l="ls -CF"
alias x="exit"
alias src="source ~/.zshrc && tmux source-file ~/.tmux.conf"
alias cs="vi ~/aliases.sh"
alias csc="vi ~/common-logic.sh"
alias csf="csc"
alias csz="vi ~/.zshrc"
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

# Notes
alias private_notes="cd ~/Desktop/private-notes"
alias pnotes="private_notes"
alias notes="private_notes"

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
