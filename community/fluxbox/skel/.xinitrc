#!/bin/sh
# ~/.xinitrc
# Executed by startx (run your window manager from here)

## Ensure that GTK themes are applied uniformly in the Desktop Environment
export GTK2_RC_FILES="$HOME/.gtkrc-2.0"

exec startfluxbox
