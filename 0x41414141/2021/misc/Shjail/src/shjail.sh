#!/bin/bash
RED='\e[0;31m'
END='\e[0m'
GREEN='\e[0;32m'

while :
do
    echo "What would you like to say?"
	read USER_INP
       	if [[ "$USER_INP" =~ ['&''$''`''>''<''/''*''?'txcsbqi] ]]; then
               	echo -e "${RED}Hmmmm, what are you trying to do?${END}"
       	else
               	OUTPUT=$($USER_INP) &>/dev/null
               	echo -e "${GREEN}The command has been executed. Let's go again!${END}"
       	fi
done 


