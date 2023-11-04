#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4471)
    echo -n '1' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    
    if [[ -e /tmp/pong/backhand ]] ; then 
        rm /tmp/pong/backhand
        touch /tmp/ping/drop_shot
    fi 

    M="$( echo -en "$M" | head -n -2 )"
    echo -en "$M" | netcat -N 127.0.0.1 4457
    
done
