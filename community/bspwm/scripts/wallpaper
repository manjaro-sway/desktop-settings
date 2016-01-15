#!/bin/sh

if ! [ -f "$HOME/.dmenurc" ]; then
	cp /usr/share/dmenu/dmenurc $HOME/.dmenurc
fi
. $HOME/.dmenurc

DMENU="dmenu $DMENU_OPTIONS -l 10 -w 800 -y $PANEL_HEIGHT"

WALLPAPER_DIR="/usr/share/backgrounds"
WALLPAPER=`ls $WALLPAPER_DIR \
	| $DMENU -p "Choose a Wallpaper :"`

FEH="feh --bg-scale"

$FEH $WALLPAPER_DIR/$WALLPAPER
