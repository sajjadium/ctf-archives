#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4450)
    C=$(cat /tmp/path)
    C=${C:0-1}
    P=$((4260 + 2*$(printf '%d' "'$C")))
    echo -n 'g' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -a /tmp/pong/backhand ]] ; then 
        rm /tmp/pong/backhand
        touch /tmp/ping/kill
        M="$( echo -en "$M" | head -n -1 )"
    fi 

    if [[ -O /tmp/ping/drop_shot ]] ; then 
        rm /tmp/ping/drop_shot
        touch /tmp/pong/kill
        M="$( echo -en "$M" | head -n -1 )"
    fi

    echo -en "$M" | netcat -N 127.0.0.1 $P
    
done
