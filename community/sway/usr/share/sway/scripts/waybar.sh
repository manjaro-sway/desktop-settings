#!/bin/sh
# wrapper script for waybar with args, see https://github.com/swaywm/sway/issues/5724

USER_CONFIG_PATH=$HOME/.config/waybar/config.jsonc

if [ -f $USER_CONFIG_PATH ]; then
    USER_CONFIG=$USER_CONFIG_PATH
fi

waybar -c ${USER_CONFIG:-"/usr/share/sway/templates/waybar/config.jsonc"}