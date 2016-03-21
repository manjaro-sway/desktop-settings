#!/bin/sh
#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)

if [ -d /etc/X11/xinit/xinitrc.d ]; then
  for f in /etc/X11/xinit/xinitrc.d/*; do
    [ -x "$f" ] && . "$f"
  done
  unset f
fi

export GTK2_RC_FILES="$HOME/.gtkrc-2.0"

DEFAULT_SESSION='i3 --shmlog-size 0'

case $1 in
  awesome       ) exec dbus-launch awesome ;;
  bspwm         ) exec dbus-launch bspwm-session ;;
  budgie        ) exec dbus-launch budgie-desktop ;;
  cinnamon      ) exec dbus-launch cinnamon-session ;;
  deepin        ) exec dbus-launch startdde ;;
  enlightenment ) exec dbus-launch enlightenment_start ;;
  fluxbox       ) exec dbus-launch startfluxbox ;;
  gnome         ) exec dbus-launch gnome-session ;;
  i3|i3wm       ) exec dbus-launch i3 --shmlog-size 0 ;;
  jwm           ) exec dbus-launch jwm ;;
  kde           ) exec dbus-launch startkde ;;
  lxde          ) exec dbus-launch startlxde ;;
  lxqt          ) exec dbus-launch lxqt-session ;;
  mate          ) exec dbus-launch mate-session ;;
  xfce          ) exec dbus-launch xfce4-session ;;

  *             ) exec dbus-launch $DEFAULT_SESSION ;;
esac
