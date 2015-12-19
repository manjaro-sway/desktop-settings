[ -r /etc/profile.d/cnf.sh ] && . /etc/profile.d/cnf.sh

source /usr/share/zsh/plugins/zsh-history-substring-search/zsh-history-substring-search.zsh

TERM=xterm
case $TERM in
  xterm*)
    precmd () {print -Pn "\e]0;%n@%m: %~\a"}
    ;;
esac
# preexec is called just before any command line is executed
function preexec() {
  title "$1" "%m(%35<...<%~)"
}

function title() {
  # escape '%' chars in $1, make nonprintables visible
  a=${(V)1//\%/\%\%}

  # Truncate command, and join lines.
  a=$(print -Pn "%40>...>$a" | tr -d "\n")

  case $TERM in
  screen)
    print -Pn "\e]2;$a@$2\a" # plain xterm title
    print -Pn "\ek$a\e\\"      # screen title (in ^A")
    print -Pn "\e_$2   \e\\"   # screen location
    ;;
  xterm*|rxvt)
    print -Pn "\e]2;$a@$2\a" # plain xterm title
    ;;
  esac
}

#zmodload zsh/terminfo
autoload -U compinit colors zcalc
compinit
colors

setopt correct          # Auto correct mistakes
setopt extendedglob     # Extended globbing
setopt nocaseglob       # Case insensitive globbing
setopt rcexpandparam    # Array expension with parameters
setopt nocheckjobs      # Don't warn about running processes when exiting
setopt numericglobsort  # Sort filenames numerically when it makes sense
setopt nohup            # Don't kill processes when exiting
setopt nobeep           # No beep
setopt appendhistory    # Immediately append history instead of overwriting
setopt histignorealldups #If a new command is a duplicate, remove the older one
setopt autocd 

zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'       # Case insensitive tab completion
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"         # Colored completion (different colors for dirs/files/etc)

bindkey -e
bindkey '^[[7~' beginning-of-line                   # Home key
bindkey '^[[8~' end-of-line                         # End key
bindkey '^[[2~' overwrite-mode                      # Insert key
bindkey '^[[3~' delete-char                         # Delete key
# bind UP and DOWN arrow keys
zmodload zsh/terminfo
bindkey "$terminfo[kcuu1]" history-substring-search-up
bindkey "$terminfo[kcud1]" history-substring-search-down
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down
bindkey '^[[C'  forward-char                        # Right key
bindkey '^[[D'  backward-char                       # Left key
bindkey '^[[5~' history-beginning-search-backward   # Page up key
bindkey '^[[6~' history-beginning-search-forward    # Page down key
bindkey '^[Oc' forward-word
bindkey '^[Od' backward-word
bindkey '^H' backward-kill-word

HISTFILE=~/.zhistory
HISTSIZE=10000
SAVEHIST=10000

alias sudo='sudo '
alias ls='ls --group-directories-first --time-style=+"%d.%m.%Y %H:%M" --color=auto -F'
alias ll='ls -l --group-directories-first --time-style=+"%d.%m.%Y %H:%M" --color=auto -F'
alias la='ls -la --group-directories-first --time-style=+"%d.%m.%Y %H:%M" --color=auto -F'
alias grep='grep --color=tty -d skip'
alias cp="cp -i"                        # Confirm before overwriting something
alias df='df -h'                        # Human-readable sizes
alias free='free -m'                    # Show sizes in MB
alias fixit='sudo rm -f /var/lib/pacman/db.lck && sudo pacman-mirrors -g && sudo pacman -Syyuu && sudo pacman -Suu'
alias bspwmrc='nano ~/.config/bspwm/bspwmrc'
alias sxhkdrc='nano ~/.config/sxhkd/sxhkdrc'
alias x='startx ~/.xinitrc' # Type name of desired desktop after x, xinitrc is configured for it
alias autostart='nano ~/.config/bspwm/autostart'
alias repoup='repo-add local-repo.db.tar.gz *.pkg.tar.*'

# ex - archive extractor
# usage: ex <file>
ex() {
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xjf $1   ;;
      *.tar.gz)    tar xzf $1   ;;
      *.bz2)       bunzip2 $1   ;;
      *.rar)       unrar x $1     ;;
      *.gz)        gunzip $1    ;;
      *.tar)       tar xf $1    ;;
      *.tbz2)      tar xjf $1   ;;
      *.tgz)       tar xzf $1   ;;
      *.zip)       unzip $1     ;;
      *.Z)         uncompress $1;;
      *.7z)        7z x $1      ;;
      *)           echo "'$1' cannot be extracted via ex()" ;;
    esac
  else
    echo "'$1' is not a valid file"
  fi
}

cleanse() {
        sudo pacman -Rns $(pacman -Qtdq) ;
        sudo pacman -Scc ;
        sudo pacman-optimize ;
        bleachbit -c --preset ;
        sudo bleachbit -c --preset
}

PROMPT="┌─[%n@%M]-[%4~]%(!.#.$) 
└─>>  "
RPROMPT="%(?.%{$fg[green]%}✓ %{$reset_color%}.%{$fg[red]%}✗ %{$reset_color%})"

#source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

