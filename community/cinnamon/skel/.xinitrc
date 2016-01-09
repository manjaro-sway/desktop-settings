#!/bin/sh

#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)
#

export GTK2_RC_FILES="$HOME/.gtkrc-2.0"

DEFAULT_SESSION=cinnamon-session
case $1 in
  cinnamon) exec dbus-launch cinnamon-session ;;
  xfce) exec dbus-launch xfce4-session ;;
  gnome) exec dbus-launch gnome-session ::
  i3) exec dbus-launch i3 ;;
  *) exec dbus-launch  $DEFAULT_SESSION ;;
esac
