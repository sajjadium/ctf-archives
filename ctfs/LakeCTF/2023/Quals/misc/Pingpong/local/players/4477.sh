#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4477)
    
    C=$(cat /tmp/path)
    C=${C:0-1}
    P=$((4479 - 3*$(printf '%d' "'$C")/11))

    echo -n '7' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -f /tmp/pong/backhand ]] ; then 
        rm /tmp/pong/backhand
        touch /tmp/ping/backhand
    fi
    
    if [[ -f /tmp/ping/drop_shot ]] ; then 
        rm /tmp/ping/drop_shot
        touch /tmp/pong/cross_court
    fi 

    if [[ -c /dev/zero ]] ; then 
        M=${M//"tr"/'3'}
    fi


    echo -en "$M" | netcat -N 127.0.0.1 $P
    
done
