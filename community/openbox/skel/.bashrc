if [ -f /etc/bash_completion ]; then
         . /etc/bash_completion
fi

xhost +local:root > /dev/null 2>&1

complete -cf sudo

shopt -s cdspell
shopt -s checkwinsize
shopt -s cmdhist
shopt -s dotglob
shopt -s expand_aliases
shopt -s extglob
shopt -s histappend
shopt -s hostcomplete
shopt -s nocaseglob

export HISTSIZE=10000
export HISTFILESIZE=${HISTSIZE}
export HISTCONTROL=ignoreboth

# Alias system

alias ls='ls --group-directories-first --time-style=+"%d.%m.%Y %H:%M" --color=auto -F'
alias ll='ls -l --group-directories-first --time-style=+"%d.%m.%Y %H:%M" --color=auto -F'
alias la='ls -la --group-directories-first --time-style=+"%d.%m.%Y %H:%M" --color=auto -F'
alias grep='grep --color=tty -d skip'
alias cp="cp -i"                          # confirm before overwriting something
alias df='df -h'                          # human-readable sizes
alias free='free -m'                      # show sizes in MB
alias np='nano PKGBUILD'

# Alias programmed 

alias update='sudo pacman -Syyuu'	# update system
alias install='sudo pacman -S'		# install package (obs.: install namepackage)
alias remove='sudo pacman -Rsn'		# remove package + dependences (obs.: remove namepackage)
alias helppacman='man pacman'		# pacman help
alias updateaur='yaourt -Syyuua'	# update aur
alias installaur='yaourt -S'		# install package aur (obs.: installaur namepackage)
alias removeaur='yaourt -Rsn'		# remove package aur + dependences (obs.: removeaur namepackage)
alias helpaur='man yaourt'		# yaourt help
alias errordb='sudo rm -f /var/lib/pacman/db.lck && sudo pacman-mirrors -g && sudo pacman -Syyuu  && sudo pacman -Suu'		# unlock data the pacman (error db.lck) and update
alias opupdate='sudo pacman-optimize && sudo pacman-mirrors -g && sudo pacman -Syyuu  && sudo pacman -Suu'	# optimize data the pacman and update
alias usbiso='sudo mkusb'		# writes ISO in pendrive (obs.: usbiso nameiso)

# ex - archive extractor
# usage: ex <file>
  ex ()
    {
      if [ -f $1 ] ; then
        case $1 in
          *.tar.bz2)   tar xjf $1   ;;
          *.tar.gz)    tar xzf $1   ;;
          *.bz2)       bunzip2 $1   ;;
          *.rar)       unrar x $1     ;;
          *.gz)        gunzip $1    ;;
          *.tar)       tar xf $1    ;;
          *.tbz2)      tar xjf $1   ;;
          *.tgz)       tar xzf $1   ;;
          *.zip)       unzip $1     ;;
          *.Z)         uncompress $1;;
          *.7z)        7z x $1      ;;
          *)           echo "'$1' cannot be extracted via ex()" ;;
        esac
      else
        echo "'$1' is not a valid file"
      fi
    }

# prompt
PS1='┌─[\d][\u@\h:\w]\n└─> '
BROWSER=/usr/bin/xdg-open