
#!/bin/sh

#
# ~/.extend.xinitrc
#
# Executed by startx (run your window manager from here)
#

# export GTK2_RC_FILES="$HOME/.gtkrc-2.0"

DEFAULT_SESSION=mate-session

export GTK_IM_MODULE=ibus
export XMODIFIERS=@im=ibus
export QT_IM_MODULE=ibus

ibus-daemon -drx
