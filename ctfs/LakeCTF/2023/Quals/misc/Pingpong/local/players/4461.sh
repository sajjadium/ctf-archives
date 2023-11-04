#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4461)
    echo -n 'r' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -o xtrace || -o errexit ]] ; then
        
        touch /tmp/ping/${M:6:3}
        M=${M:0:6}${M:9}
    
    fi

    if [[ -w /tmp/ping/backhand ]] ; then 
        rm /tmp/ping/backhand
        touch /tmp/pong/backhand
        M="$( echo -en "$M" | head -n -1 )"
    fi 
    
    echo -en "$M" | netcat -N 127.0.0.1 4454
    
done
