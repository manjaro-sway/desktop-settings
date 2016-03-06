#
# ~/.extend.bashrc
#

for sd_cmd in systemctl systemd-analyze systemd-run; do
    alias $sd_cmd='DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/dbus/user_bus_socket" '$sd_cmd
done

xhost +local:root > /dev/null 2>&1

complete -cf sudo

export BROWSER=/usr/bin/epiphany
export EDITOR=/usr/bin/nano
export HISTSIZE=1000
export HISTFILESIZE=${HISTSIZE}
export HISTCONTROL=ignoreboth
export JAVA_FONTS=/usr/share/fonts/TTF
# Bash won't get SIGWINCH if another process is in the foreground.
# Enable checkwinsize so that bash will check the terminal size when
# it regains control.  #65623
# http://cnswww.cns.cwru.edu/~chet/bash/FAQ (E11)
shopt -s checkwinsize
shopt -s cdspell
shopt -s expand_aliases
shopt -s cmdhist
shopt -s dotglob
shopt -s extglob

alias cp="cp -i"                          # confirm before overwriting something
alias df='df -h'                          # human-readable sizes
alias free='free -m'                      # show sizes in MB
alias np='nano -w PKGBUILD'
alias more=less
alias fixit='sudo rm -f /var/lib/pacman/db.lck && sudo pacman-mirrors -g && sudo pacman -Syyuu && sudo pacman -Suu'
alias bspwmrc='nano ~/.config/bspwm/bspwmrc'
alias sxhkdrc='nano ~/.config/sxhkd/sxhkdrc'
alias autostart='nano ~/.config/bspwm/autostart'
alias x='startx ~/.xinitrc'
# export QT_SELECT=4

# Enable history appending instead of overwriting.  #139609
shopt -s histappend

#Command-not-found hook. Requires package command-not-found
[ -r /etc/profile.d/cnf.sh ] && . /etc/profile.d/cnf.sh
