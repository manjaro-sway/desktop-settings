#!/bin/sh
# wrapper script for foot

USER_CONFIG_PATH=${HOME}/.config/foot/foot.ini

if [ -f $USER_CONFIG_PATH ]; then
    USER_CONFIG=$USER_CONFIG_PATH
fi

foot -D $(/usr/share/sway/scripts/swaycwd.sh) -c ${USER_CONFIG:-"/usr/share/sway/templates/foot.ini"} $@ &
