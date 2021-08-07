#!/bin/bash
targetSearch="
/etc/sway/modes/
/etc/sway/definitions"

accent_color="#ffffff8e"
text_color="#ffffff8e"

count="0"
echo '<span size="13000" face="monospace" foreground="'$text_color'">'
grep -h -r "bindsym" $targetSearch \
	| grep '###' \
	| grep -v 'unbindsym' \
	| sed 's/\$bindsym/bindsym --to-code/g' \
	| sed 's/^\s*//' \
	| sed 's/\$mod/Win/g' \
	| sed 's/Left/←/' \
	| sed 's/Right/→/' \
	| sed 's/Down/↓/' \
	| sed 's/Up/↑/' \
	| sed '$a bindsym' \
	| while read line; do
	description_new=$(echo $line | grep -o '###.*$' |  tr -d "###")	
	combination_new=$(echo $line | grep -o -e "\-\-to\-code [^ ]*" | sed 's/--to-code//' | sed 's/^ *//')
	
	if [[ "$description_new" = "$description" && "$description_new" != "" ]]
	then 
		combination=$(echo $combination $combination_new \
		| sed 's/+/\n/g' | sed 's/ /\n@\n/g' \
		| awk '!($0 in a)||/@/ {a[$0];print}' \
		| xargs | sed 's/ /+/g' | sed 's/+@+//g'\
		)
	else
		if [ -n "$combination" ]; 
		then
			printf "<span foreground=\"$accent_color\"><b>%s</b></span>@@@%s " "$combination" "$description"
			if [[ "$count" = "0" ]];
			then
				printf "@@@"			
				count="1"
			else
				printf "\n"
				count="0"
			fi
		fi
		combination=$combination_new
		description=$description_new
	fi
done | column -t -o " " -s "@@@"
echo '</span>'
