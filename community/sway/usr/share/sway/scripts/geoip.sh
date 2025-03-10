#!/bin/sh
set -xu

GEO_CONTENT=$(curl -sL https://manjaro-sway.download/geoip)
if [ "$GEO_CONTENT" != ""]; then
    echo $GEO_CONTENT >"$HOME/.cache/geoip"
elif [ -f "$HOME/.cache/geoip" ]; then
    GEO_CONTENT=$(cat "$HOME/.cache/geoip")
fi

if [ "$GEO_CONTENT" != "" ]; then
    echo $GEO_CONTENT
    exit 0
fi

exit 1
