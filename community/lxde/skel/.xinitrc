
#!/bin/sh

#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)
#

export GTK2_RC_FILES="$HOME/.gtkrc-2.0"

DEFAULT_SESSION=startlxde
case $1 in
  lxde) exec  ck-launch-session dbus-launch startlxde ;;
  *) exec ck-launch-session dbus-launch  $DEFAULT_SESSION ;;
esac

# fix pcmanfm
dbus-launch pcmanfm
