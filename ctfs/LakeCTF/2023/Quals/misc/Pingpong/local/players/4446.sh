#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4446)
    echo -n 'c' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    
    if [[ -u /tmp/pong/drop_shot || -k /tmp/pong/drop_shot ]] ; then 
        rm /tmp/pong/drop_shot
        touch /tmp/ping/forehand
        M="$( echo -en "$M" | head -n -2 )"
    fi
    if [[ -G /tmp/pong/drop_shot ]] ; then 
        rm /tmp/pong/drop_shot
        touch /tmp/ping/loop
        M="$( echo -en "$M" | head -n -1 )"
    fi
    M=${M//'r'/'5'}
    
    echo -en "$M" | netcat -N 127.0.0.1 4464
done
