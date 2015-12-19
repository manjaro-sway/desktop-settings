#!/bin/sh
#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)
#
#
## Ensure that the D-Bus Communication System is running properly to fix
## File management, authentication, and other essential system processes (I)

if [ -d /etc/X11/xinit/xinitrc.d ]; then
  for f in /etc/X11/xinit/xinitrc.d/*; do
    [ -x "$f" ] && . "$f"
  done
  unset f
fi

## Ensure that GTK themes are applied uniformly in the Desktop Environment

export GTK2_RC_FILES="$HOME/.gtkrc-2.0"

## Ensure that the D-Bus Communication System is running properly to fix
## File management, authentication, and other essential system processes (II)

if which dbus-launch >/dev/null && test -z "$DBUS_SESSION_BUS_ADDRESS"; then
    eval "$(dbus-launch --sh-syntax --exit-with-session)"
fi

## Where the default Home folders have not already been created, generate them

if [ -x /usr/bin/xdg-user-dirs-update ]; then
   /usr/bin/xdg-user-dirs-update
fi

## Enable SLiM to enable selection of multiple desktop environments, or
## set a single session. Only one or the other must be unhashed! In either
## instance, /etc/slim.conf must also be amended accordingly.
## Enable multiple desktop environments

#exec $1

## Set a single desktop environment

exec /usr/bin/jwm
