#!/bin/sh
#
# ~/.extend.xinitrc
#
# Executed by startx (run your window manager from here)

[[ -f ~/.Xdefaults ]] && xrdb -merge ~/.Xdefaults

DMENU_FN="Terminus-15"
DMENU_NB="#000000"
DMENU_NF="#99CC99"
DMENU_SB="#99CC99"
DMENU_SF="#000000"
DMENU_OPTIONS="-fn $DMENU_FN -nb $DMENU_NB -nf $DMENU_NF -sf $DMENU_SF -sb $DMENU_SB"
#export DMENU_FN DMENU_NB DMENU_NF DMENU_SF DMENU_SB DMENU_OPTIONS
export GTK2_RC_FILES="$HOME/.gtkrc-2.0"

 #Bspwm is kept as default
DEFAULT_SESSION=bspwm-session
