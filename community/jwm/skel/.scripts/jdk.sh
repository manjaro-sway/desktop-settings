#!/bin/bash
#
# Simple bash script install Java support
# 
# Written by Carl Duff (adapted holmeslinux)

# Information about this script for the user
echo "${title}Install Java support${nrml}.

This will install the necessary software to run Java.

Press ${grnb}<enter>${nrml} to proceed. You may still cancel the process when prompted."

read
pacman -S jre8-openjdk jre8-openjdk-headless icedtea-web
read -p $'\n'"Process Complete. Press ${grnb}<enter>${nrml} to continue."$'\n'
exit 0