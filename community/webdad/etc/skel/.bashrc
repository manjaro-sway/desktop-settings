if [ ! -f "/etc/jde/live-iso" ]; then
    if [ -f "/usr/bin/fish" ]; then 
        echo -e "\e[92m Checking for updates \033[0m"
        fish
    else
        echo "Welcome, this will only run once"
        echo "Upgrading the shell for humans by installing fish"
        echo -e "\033[31m Make sure you are connected to the internet \033[0m"
        echo -e "\e[92m Installing Fish \033[0m"
        sudo pacman -Sy --noconfirm fish
        echo "\e[92m Instaling oh my fish plugin \033[0m"
        curl -L https://get.oh-my.fish > installomf
        fish installomf
    fi
fi
