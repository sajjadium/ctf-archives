#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4478)
    echo -n '8' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    touch /tmp/ping/serve

    if [[ -h /tmp/pong/backhand ]] ; then 
        rm /tmp/pong/backhand
        touch /tmp/ping/backhand
    fi

    if [[ -a /tmp/pong/forehand ]] ; then
        M=${M//'e'/'8'}
    fi
    
    echo -en "$M" | netcat -N 127.0.0.1 4479
    
done
