#!/bin/bash
#
# Simple bash script to install firewall support
#
# Written by Carl Duff (adapted holmeslinux) 

# Information about this script for the user
echo "${title}Install and enable firewall support${nrml}.

This will install the necessary software to run firewall.

Press ${grnb}<enter>${nrml} to proceed. You may still cancel the process when prompted."

read
pacman -S gufw ufw && systemctl enable ufw -f && systemctl start ufw && ufw enable && ufw status
read -p $'\n'"Process Complete. Press ${grnb}<enter>${nrml} to continue."$'\n'
exit 0