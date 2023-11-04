#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4460)
    C=${M:0-1}
    
    L=$(printf '%d' "'$C")
    echo -n 'q' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    
    P=$(($L*100))

    if [[ -f /tmp/ping/loop ]] ; then 
        rm /tmp/ping/loop
        touch /tmp/pong/fronthand
    fi

    if [[ -a /tmp/pong/serve ]] ; then 
        rm /tmp/pong/serve
        touch /tmp/ping/loop
    fi 

    echo -en "$M" | netcat -N 127.0.0.1 "$P"

done
