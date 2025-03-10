#!/usr/bin/env bash
set -xu

LOCKFILE="$HOME/.local/auto-theme-toggle"
DARK_SWAY_THEME="$HOME/.config/sway/definitions.d/theme.dark.conf_"
LIGHT_SWAY_THEME="$HOME/.config/sway/definitions.d/theme.light.conf_"

PRIMARY_THEME="dark"
SECONDARY_THEME="light"
NEXT_PRIMARY_THEME="dark"
NEXT_SECONDARY_THEME="light"

if [ -f "$DARK_SWAY_THEME" ]; then
    PRIMARY_THEME="light"
    SECONDARY_THEME="dark"
fi

AUTO_TOGGLE="false"
if [ -f "$LOCKFILE" ]; then
    AUTO_TOGGLE="true"
fi

if [ "$AUTO_TOGGLE" == "true" ]; then
    GEO_CONTENT=$(sh /usr/share/sway/scripts/geoip.sh)
    sunrise_string=$(echo "$GEO_CONTENT" | jq -r '.sunrise // empty')
    sunset_string=$(echo "$GEO_CONTENT" | jq -r '.sunset // empty')
    sunrise_unix=$(date -d "$sunrise_string" +%s)
    sunset_unix=$(date -d "$sunset_string" +%s)
    current_unix=$(date +%s)
    if [ $current_unix -ge $sunrise_unix ] && [ $current_unix -lt $sunset_unix ]; then
        NEXT_PRIMARY_THEME="light"
        NEXT_SECONDARY_THEME="dark"
    else
        NEXT_PRIMARY_THEME="dark"
        NEXT_SECONDARY_THEME="light"
    fi
fi

#Accepts managing parameter
case $1'' in
'toggle')
    if [ "$AUTO_TOGGLE" != "true" ]; then
        NEXT_PRIMARY_THEME="$SECONDARY_THEME"
        NEXT_SECONDARY_THEME="$PRIMARY_THEME"
    fi
    ;;
'auto-toggle')
    if [ -f "$LOCKFILE" ]; then
        rm "$LOCKFILE"
    else
        touch "$LOCKFILE"
    fi
    ;;
'check')
    [ -f "$DARK_SWAY_THEME" ] || [ -f "$LIGHT_SWAY_THEME" ]
    exit $?
    ;;
'status')
    #Returns a string for Waybar
    text="switch to ${SECONDARY_THEME} theme\r(Right click to switch automatically)"
    alt=$PRIMARY_THEME
    if [ "$AUTO_TOGGLE" == "true" ]; then
        hours=$((($sunset_unix - $current_unix) / (60 * 60)))
        text="switching to ${SECONDARY_THEME} theme in ${hours} hours\r(Right click to disable)"
        alt="auto"
    fi

    printf '{"alt":"%s","tooltip":"%s"}\n' "$alt" "$text"
    exit 0
    ;;
esac

if [ "$PRIMARY_THEME" == "$NEXT_PRIMARY_THEME" ]; then
    exit 0
fi

PRIMARY_SWAY_THEME="$HOME/.config/sway/definitions.d/theme.conf"
PRIMARY_FOOT_THEME="$HOME/.config/foot/foot-theme.ini"
/usr/bin/mv --backup -v $PRIMARY_SWAY_THEME "$HOME/.config/sway/definitions.d/theme.${NEXT_SECONDARY_THEME}.conf_"
/usr/bin/mv --backup -v $PRIMARY_FOOT_THEME "$HOME/.config/foot/foot-theme.${NEXT_SECONDARY_THEME}.ini_"
/usr/bin/mv --backup -v "$HOME/.config/sway/definitions.d/theme.${NEXT_PRIMARY_THEME}.conf_" $PRIMARY_SWAY_THEME
/usr/bin/mv --backup -v "$HOME/.config/foot/foot-theme.${NEXT_PRIMARY_THEME}.ini_" $PRIMARY_FOOT_THEME

waybar-signal theme
swaymsg reload
