#!/bin/bash
#
# Simple bash script install multimedia support
#
# Written by Carl Duff (adapted holmeslinux)

# Information about this script for the user
echo "${title}Install multimedia support${nrml}.

This will install the necessary software to run multimedia.

Press ${grnb}<enter>${nrml} to proceed. You may still cancel the process when prompted."

read
pacman -S gst-libav gst-plugins-bad gst-plugins-base gst-plugins-good gst-plugins-ugly gstreamer0.10-bad-plugins gstreamer0.10-base-plugins gstreamer0.10-good-plugins
gstreamer0.10-ugly-plugins flashplugin libdvdcss flac
read -p $'\n'"Process Complete. Press ${grnb}<enter>${nrml} to continue."$'\n'
exit 0