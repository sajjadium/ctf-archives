#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4470)
    echo -n '0' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -x /tmp/ping/spin ]] ; then 
        rm /tmp/ping/spin
        touch /tmp/pong/drop_shot
    fi

    if [[ -f /tmp/ping/serve ]] ; then 
        rm /tmp/ping/serve
        touch /tmp/pong/cross_court
    fi
 
    M=${M:0:4}0${M:4}
    M="$( echo -en "$M" | head -n -2 )"

    echo -en "$M" | netcat -N 127.0.0.1 4457
    
done
