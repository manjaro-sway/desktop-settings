# base config for oh my zsh
source /usr/share/oh-my-zsh/zshrc

# Source manjaro config
source ~/.zshrc

# user-defined overrides
[ -d ~/.config/zsh/config.d/ ] && source ~/.config/zsh/config.d/*

# Fix for foot terminfo not installed on most servers
alias ssh="TERM=xterm-256color ssh"
