#
# ~/.extend.bashrc
#

# to avoid xdg-open fork-bomb, export $BROWSER from here
export BROWSER=/usr/bin/palemoon

# greetings
echo Hello, welcome to Manjaro JWM Community Edition!

# prompt programmed
PS1="\[\e[0;1m\]┌─(\[\e[31;1m\]\u\[\e[0;1m\]) > {\[\e[36;1m\]\w\[\e[0;1m\]}\n└──┤ \[\e[0m\]"
