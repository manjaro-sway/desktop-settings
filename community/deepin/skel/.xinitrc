#!/bin/sh
#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)

if [ -d /etc/X11/xinit/xinitrc.d ] ; then
    for f in /etc/X11/xinit/xinitrc.d/?* ; do
        [ -x "$f" ] && . "$f"
    done
    unset f
fi

export GTK2_RC_FILES="$HOME/.gtkrc-2.0"

DEFAULT_SESSION=deepin
case $1 in
  deepin) exec dbus-launch startdde ;;
  *) exec dbus-launch  $DEFAULT_SESSION ;;
esac
