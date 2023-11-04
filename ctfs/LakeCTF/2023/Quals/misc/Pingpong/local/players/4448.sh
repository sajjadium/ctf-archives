#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4448)
    echo -n 'e' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -r /tmp/pong/cross_court ]] ; then 
        rm /tmp/pong/cross_court
        touch /tmp/ping/drop_shot
    fi

    if [[ -w /tmp/ping/backhand ]] ; then 
        rm /tmp/ping/backhand
        touch /tmp/pong/smash
    fi
    
    echo -en "$M" | netcat -N 127.0.0.1 4480
done
