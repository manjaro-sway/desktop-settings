#!/bin/bash
#
# Simple bash script to install AUR support
#
# Written by Carl Duff (adapted holmeslinux)

# Information about this script for the user
echo "${title}Install AUR support${nrml}

This will install the necessary software to run AUR

Press ${grnb}<enter>${nrml} to proceed. You may still cancel the process when prompted."

read
pacman -S autoconf automake binutils bison fakeroot flex gcc libtool m4 make patch yaourt
read -p $'\n'"Process Complete. Press ${grnb}<enter>${nrml} to continue"$'\n'
exit 0