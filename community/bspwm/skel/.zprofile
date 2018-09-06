PATH="/usr/local/sbin:/usr/bin/core_perl:/usr/local/bin:/usr/bin:$HOME/.config/bspwm/panel:$HOME/.bin"
source $HOME/.profile
export PANEL_FIFO="/tmp/panel-fifo"
export PATH
export XDG_CONFIG_HOME="$HOME/.config"
export BSPWM_SOCKET="/tmp/bspwm-socket"
export XDG_CONFIG_DIRS=/usr/etc/xdg:/etc/xdg
export PANEL_FIFO PANEL_HEIGHT PANEL_FONT_FAMILY
#[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && exec starx
# Following automatically calls "startx" when you login:
[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && exec startx -- -keeptty -nolisten tcp > ~/.xorg.log 2>&1
