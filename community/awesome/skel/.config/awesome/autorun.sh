#!/usr/bin/env bash

function run {
  if ! pgrep $1 ; then
    $@&
  fi
}
run nm-applet
run dbus-launch update-checker
run light-locker
run pulseaudio -D
run compton --shadow-exclude '!focused'
run xcape -e 'Super_L=Super_L|Shift_L|p'
run lxpolkit
run thunar --daemon
run urxvtd
run xfce4-power-manager
run pa-applet
run xrdb merge ~/.Xresources
