#!/usr/bin/env bash
# Copied over from https://aur.archlinux.org/packages/swaycwd/
# version: swaycwd 1.1-1


fallback="$HOME"

# taken from https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash
! PARSED=$(getopt --options="h?f:" --longoptions="fallback:,help" --name "$0" -- "$@")
if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
    # e.g. return value is 1
    #  then getopt has complained about wrong arguments to stdout
    exit 2
fi

# helptext 
usage="$(basename $0) [-h] [-f=/fallback/directory] 

Get Current Working Directory for program under cursor in sway. 

Options: 
 -h, --help     Print this help text
 -f, --fallback Set directory to print when error occured (defaults to $HOME)"

# parse args
eval set -- "$PARSED"

while true; do
	case "$1" in 
	-f|--fallback) 
		fallback="$2"
		shift 2
		;;
	-h|--help)
		echo "$usage"
		exit 0
		;;
	--)
		break
		;;
	*) 
		echo "argparse error"
		exit 1
		;;
	esac
done

# get parent pid of program under cursor
pid=$(swaymsg -t get_tree | jq '.. | select(.type?) | select(.type=="con") | select(.focused==true).pid')
ppid=$(pgrep --newest --parent ${pid})

# get cwd from proc dir
location=$(readlink /proc/${ppid}/cwd)

if [ "$?" -ne 0 ]; then 
	# just print out fallback dir on error
	echo $fallback
	exit 0
fi 

# find out if the path points to /proc dir
# use fallback in that case
echo $location | grep -q /proc && echo $fallback || echo $location
