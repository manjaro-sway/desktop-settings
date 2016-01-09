#!/bin/bash

if zenity --question --title="Swap to NetworkManager" --text="This is for swapping from Connman+EConnman to NetworkManager+NM-applet.\n\n<b>If your networking is operating fine right now then you don't need to and should not run this.</b>\nJust keep using Connman, which is best supported within Enlightenment.\n\nOnly people on particular mobile broadband hardware or perhaps users who connect to\ncorporate/enterprise wifi would need this.\nYou can delete the text file off your desktop if you don't need it.\n\n\n<b>Do you really want to swap to NetworkManager?</b>"; then
  terminology -e gksu /opt/manjaro-enlightenment/nm-swap.sh
  if [ "$(grep -i '/etc/xdg/autostart/nm-applet.desktop' ~/.e/e/applications/startup/.order)" == "" ]; then
    echo "/etc/xdg/autostart/nm-applet.desktop" >> ~/.e/e/applications/startup/.order
  fi
  cd /tmp
  if [ "$(ps -A | grep -i 'nm-applet')" == "" ]; then
    nohup nm-applet &
  fi
  zenity --info --text="Now remove the Econnman item from your shelf.\nAt this point it should look like an exclamation mark.\n\nThe NetworkManager applet icon should already be in your system tray area."
fi
