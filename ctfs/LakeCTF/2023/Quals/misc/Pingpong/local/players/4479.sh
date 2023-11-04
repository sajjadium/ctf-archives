#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4479)
    echo -n '9' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -f /tmp/ping/serve ]] ; then 
        rm /tmp/ping/serve
        touch /tmp/pong/forehand
    fi

    if [[ -a /tmp/pong/forehand ]] ; then
        exit 9
    fi

    echo -en "$M" | netcat -N 127.0.0.1 4478
    
done
