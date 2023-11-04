#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4451)
    C=$(cat /tmp/path)
    C=${C:0-1}
    P=$((3856+ 24*($(printf '%d' "'$C")/2)))
    echo -n 'h' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    
    if [[ -r /tmp/pong/loop && -w /tmp/pong/loop ]] ; then 
        M=${M/'z'/''}
        rm /tmp/pong/loop
        touch /tmp/ping/smash
    fi
    
    if [[ -w /tmp/pong/serve ]] ; then 
        M="$( echo -en "$M" | head -n -2 )"
        rm /tmp/pong/serve
        touch /tmp/ping/smash
    fi

    M=F$M
    M="$( echo -en "$M" | head -n -1 )"
    echo -en "$M" | netcat -N 127.0.0.1 $P
done
