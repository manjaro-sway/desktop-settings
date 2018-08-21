#!/usr/bin/env bash

# run (only once) processes which spawn with the same name
function run {
   if ! pgrep $1 ; then
     $@&
   fi
}

# run (only once) processes which spawn with different name
if ! pgrep gnome-keyring-d ; then
    gnome-keyring-daemon --daemonize --login &
fi
if ! pgrep pulseaudio ; then
    start-pulseaudio-x11 &
fi
if ! pgrep polkit-mate-aut ; then
    /usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &
fi
if ! pgrep xfce4-power-man ; then
    xfce4-power-manager &
fi

run xfsettingsd
run nm-applet
run light-locker
run compton --shadow-exclude '!focused'
run xcape -e 'Super_L=Super_L|Control_L|Escape'
run thunar --daemon
run pa-applet
run pamac-tray