#!/usr/bin/env bash

RELOAD_CMD='yay -Qqu'
REMOVE_CMD='yay -Ru' 
PREVIEW_CMD='yay -Qic'
UPGRADE_CMD='yay --noconfirm -S'

yay -Syy && yay -Qqu | \
  fzf \
  --multi \
  --layout=reverse \
  --header 'Press Ctrl-S to sync, Ctrl-R to remove, Return to upgrade' \
  --preview "$PREVIEW_CMD {} 2>/dev/null" \
  --bind "ctrl-a:select-all" \
  --bind "ctrl-r:execute($REMOVE_CMD {+})+reload($RELOAD_CMD)" \
  --bind "ctrl-s:reload($RELOAD_CMD)" \
  --bind "enter:execute($UPGRADE_CMD {+})+reload($RELOAD_CMD)"
