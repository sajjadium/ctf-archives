#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4465)
    echo -n 'v' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -w /tmp/ping/dead_ball ]] ; then 
        rm /tmp/ping/dead_ball
        touch /tmp/pong/serve
    fi

    if [[ -S /tmp/pong/backhand ]] ; then 
        rm /tmp/pong/backhand
        touch /tmp/ping/fronthand
    fi
    
    echo -en "$M" | netcat -N 127.0.0.1 4467
done
