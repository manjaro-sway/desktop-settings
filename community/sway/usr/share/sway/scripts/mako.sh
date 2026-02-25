#!/usr/bin/env sh
# wrapper script for mako
USER_CONFIG_PATH="${HOME}/.config/mako/config"

if [ -f "$USER_CONFIG_PATH" ]; then
    exec mako -c "$USER_CONFIG_PATH"
else
    exec mako -c "/usr/share/sway/templates/mako" "$@"
fi
