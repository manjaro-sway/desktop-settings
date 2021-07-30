#!/bin/bash 

pid=`pgrep wf-recorder`
status=$?

gif=false

while getopts ":g:" arg; do
  case $arg in
    g)
        gif=true
        echo "will save as gif" 
        ;;
  esac
done

countdown() {
  notify "Recording in 3 seconds" -t 1000
  sleep 1
  notify "Recording in 2 seconds" -t 1000
  sleep 1
  notify "Recording in 1 seconds" -t 1000
  sleep 1
}

# set ffmpeg defaults
ffmpeg() {
    command ffmpeg -hide_banner -loglevel error -nostdin "$@"
}

video_to_gif() {
    ffmpeg -i "$1" -vf palettegen -f image2 -c:v png - |
    ffmpeg -i "$1" -i - -filter_complex paletteuse "$2"
}

notify() {
    line=$1
    shift
    notify-send "Recording" "${line}" -i /usr/share/icons/Papirus-Dark/32x32/devices/camera-video.svg $*;
}

if [ $status != 0 ]
then
    file=$(xdg-user-dir VIDEOS)/$(date +'recording_%Y%m%d-%H%M%S.mp4')

    notify "Select a region to record" -t 1000
    area=$(swaymsg -t get_tree | jq -r '.. | select(.pid? and .visible?) | .rect | "\(.x),\(.y) \(.width)x\(.height)"' | slurp)

    countdown
    wf-recorder --audio=0 -g "$area" -f $file
    notify "Finished recording ${file}"


    if [ $gif == true ]
    then
        file_gif="${file}.gif"
        notify "Converting to gif" -t 1000
        video_to_gif "${file}" "${file_gif}"
        notify "Saved as ${file_gif}"
    fi
else 
    pkill --signal SIGINT wf-recorder
fi