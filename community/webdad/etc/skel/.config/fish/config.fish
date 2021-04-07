function pink -d "Set color palette for pink theme."
    set budspencer_colors $budspencer_pink
    set budspencer_cursors "\033]12;#$budspencer_colors[10]\007" "\033]12;#$budspencer_colors[5]\007" "\033]12;#$budspencer_colors[8]\007" "\033]12;#$budspencer_colors[9]\007"
end

if test -d ~/.config/omf/
    read -x omf_theme < ~/.config/omf/theme
    if [ $omf_theme != "budspencer" ]  
        echo -e "\e[92m Installing theme \033[0m"
        omf install budspencer
        # make sure theme values change
        echo "budspencer" >> ~/.config/omf/theme
        echo -e "\e[92m Set shell colors \033[0m"
        set -U budspencer_pink 000000 083743 445659 fdf6e3 e91e63 cb4b16 dc121f af005f 6c71c4 268bd2 2aa198 859900
        echo -e "\e[92m Install plugins manager \033[0m"
        curl -sL https://git.io/fisher | source && fisher install jorgebucaran/fisher
        echo -e "\e[92m Install fish async prompt \033[0m"
        fisher install acomagu/fish-async-prompt
        echo -e "\e[92m Install Gitnow for high level async operations on top of git \033[0m"
        fisher install joseluisq/gitnow@2.8.0
        echo -e "\e[92m Install bax for better posix compability \033[0m"
        fisher install jorgebucaran/fish-bax
        pink
    else
        omf update
    end
end 
