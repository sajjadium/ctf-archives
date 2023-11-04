#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4473)
    echo -n '3' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    
    C=${M:0:1}
    
    L=$(printf '%d' "'$C")

    if [[ -s /tmp/ping/winner ]] ; then 
        cat /tmp/ping/winner | tail -c 1 >> /tmp/ping/winner
    fi

    if [[ -b /tmp/pong/backhand ]] ; then 
        rm /tmp/pong/backhand
        touch /tmp/ping/drop_shot
    fi

    if [[ -r /tmp/ping/backhand ]] ; then 
        rm /tmp/ping/backhand
        touch /tmp/pong/drop_shot
    fi
    
    if [[ $L -gt 72 ]] ; then
        M=C$M

        P=$(($L*5+4090))
        echo -en "$M" | netcat -N 127.0.0.1 $P
    else 
        P=$(($L*62 + 13)) 
        echo -en "$M" | netcat -N 127.0.0.1 $P
    fi
done
