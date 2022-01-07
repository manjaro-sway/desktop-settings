#!/bin/sh
tracking=$(zeit tracking --no-colors)

if [[ "$1" == "status" ]]
then
    text=$(echo -n $tracking | grep -q 'tracking' && echo "tracking" || echo "stopped")
    tooltip=$tracking
    echo {\"text\":\"$text\"\,\"tooltip\":\"$tooltip\"\,\"class\":\"$text\"\,\"alt\":\"$text\"}
fi

if [[ "$1" == "click" ]]
then
  if echo "$tracking" | grep -q 'tracking'
  then
    zeit finish
  else
    swaymsg exec \$zeit_list
  fi
fi

if [[ "$1" == "track" ]]
then
    input=$(cat -)
    task=$(echo $input | pcregrep -io1 '└── (.+) \[.+')
    project=$(echo $input | pcregrep -io1 '.+\[(.+)\]')

    if [[ "$task" == "" ]] || [[ "$project" == "" ]]
    then
        exit 1
    fi

    zeit track -p "$project" -t "$task"
fi
