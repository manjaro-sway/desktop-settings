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

[[ -f ~/.Xdefaults ]] && xrdb -merge ~/.Xdefaults

if which dbus-launch >/dev/null && test -z "$DBUS_SESSION_BUS_ADDRESS"; then
    eval "$(dbus-launch --sh-syntax --exit-with-session)"
fi
DMENU_FN="-zevv-peep-medium-*-normal--20-175-*-*-c-*-iso8859-15"
#DMENU_FN="-*-terminus-medium-r-normal-*-20-*-*-*-*-*-iso10646-*"
DMENU_NB="#000000"
DMENU_NF="#99CC99"
DMENU_SB="#99CC99"
DMENU_SF="#000000"
DMENU_OPTIONS="-fn $DMENU_FN -nb $DMENU_NB -nf $DMENU_NF -sf $DMENU_SF -sb $DMENU_SB"
#export DMENU_FN DMENU_NB DMENU_NF DMENU_SF DMENU_SB DMENU_OPTIONS
export GTK2_RC_FILES="$HOME/.gtkrc-2.0"
export GUI_EDITOR=gedit
export EDITOR=nano
export TERMINAL_CMD=terminal
export BROWSER=midori
if [ -x /usr/bin/xdg-user-dirs-update ]; then

   /usr/bin/xdg-user-dirs-update
fi

 #Bspwm is kept as default
session=${1:-bspwm}

case $session in
    awesome           ) exec awesome;;
    bspwm             ) exec bspwm;;
    catwm             ) exec catwm;;
    spectrwm          ) exec spectrwm;;
    cinnamon          ) exec cinnamon-session;;
    dwm               ) exec dwm;;
    enlightenment     ) exec enlightenment_start;;
    ede               ) exec startede;;
    fluxbox           ) exec startfluxbox;;
    gnome             ) exec gnome-session;;
    gnome-classic     ) exec gnome-session --session=gnome-classic;;
    i3|i3wm           ) exec i3;;
    icewm             ) exec icewm-session;;
    jwm               ) exec jwm;;
    kde               ) exec startkde;;
    mate              ) exec mate-session;;
    monster|monsterwm ) exec monsterwm;;
    notion            ) exec notion;;
    openbox           ) exec openbox-session;;
    unity             ) exec unity;;
    xfce|xfce4        ) exec startxfce4;;
    xmonad            ) exec xmonad;;
    # No known session, try to run it as command
    *) exec $1;;
esac
