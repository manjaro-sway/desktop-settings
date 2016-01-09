# Base16 Shell
eval sh $HOME/.config/base16-shell/base16-tomorrow.dark.sh

# start X at login
if status --is-login
    if test -z "$DISPLAY" -a $XDG_VTNR -eq 1
        exec startx -- -keeptty
    end
end

set fish_greeting ""

set -gx PATH $PATH ~/.bin/
