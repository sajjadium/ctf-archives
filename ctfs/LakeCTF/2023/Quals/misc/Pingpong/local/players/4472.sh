#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4472)
    echo -n '2' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    
    if [[ -s /tmp/ping/backhand ]] ; then
        rm /tmp/ping/backhand
        touch /tmp/pong/fronthand
    fi

    if [[ -s /tmp/pong/backhand ]] ; then
        rm /tmp/pong/backhand
        touch /tmp/ping/fronthand
    fi

    
    L=${#M}
    P=$(((($L*233)%5)%2+4470))
    echo -en "$M" | netcat -N 127.0.0.1 $P
done
