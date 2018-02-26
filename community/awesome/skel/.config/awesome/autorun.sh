#!/usr/bin/env bash

function run {
  if ! pgrep $1 ;
    then
        $@&
          fi
          }
run nm-applet
run update-checker
run light-locker
run pulseaudio -D
run pa-applet
run compton -D