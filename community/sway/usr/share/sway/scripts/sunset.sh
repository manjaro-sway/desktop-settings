#!/bin/sh

#Startup function
function start(){
	source $HOME/.config/wlsunset/config

	if [ ${location} = "on" ]; 
	then
		CONTENT=$(curl -s https://freegeoip.app/json/)
		longitude=${$(echo $CONTENT | jq '.longitude // empty'):-${longitude:-65}}
		latitude=${$(echo $CONTENT | jq '.latitude // empty'):-${latitude:-65}}
		wlsunset -l $latitude -L $longitude -t $temp_low -T $temp_high -d $duration &
	else
		wlsunset -t $temp_low -T $temp_high -d $duration -S $sunrise -s $sunset &
	fi
}

#Accepts managing parameter 
case $1'' in
	'off')
   	pkill wlsunset
	;;

	'on')
	start
	;;

	'toggle')
   	if pkill -0 wlsunset
	then
		pkill wlsunset
	else
		start
	fi
    ;;
    'check')
    command -v wlsunset
    exit $?
    ;;
esac

#Returns a string for Waybar 
if pkill -0 wlsunset
then
	class="on"
else
	class="off"
fi	

printf '{"alt":"%s"}\n' "$class"
