#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4459)
    C=$(cat /tmp/path)
    L=$(echo -en "$C" | wc -c )
    C=${C:0-1}
    echo -n 'p' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    
    if [[ -f /tmp/pong/dead_ball ]] ; then 
        rm /tmp/pong/dead_ball
        touch /tmp/ping/serve
    fi
    

    P=$(printf '%d' "'$C")
    if [[ $P -gt 95 ]] ; then 
        echo -n '-' >> /tmp/path
    fi
    P=$(( $P%7 + ($L*4)%5 + 4467 ))
    echo -en "$M" | netcat -N 127.0.0.1 $P
    
done
