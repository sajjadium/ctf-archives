#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4454)
    echo -n 'k' >> /tmp/path

    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    P=4451

    if [[ -G /tmp/pong/flat ]] ; then 
        rm /tmp/pong/flat
        touch /tmp/ping/loop
        P=$(($P+10))
    fi

    if [[ -x /tmp/pong/backhand ]] ; then
        rm /tmp/pong/backhand
        touch /tmp/ping/backhand
        P=$(($P+10))
    fi
    
    for FILE in $(ls /tmp/ping)
    do 
    if [[ "$FILE" =~ ^...$  && -w /tmp/ping/winner ]] ; then 
        echo -n "$FILE" >> /tmp/ping/winner 
        P=$(($P+10))
    fi
    done

    echo -en "$M" | netcat -N 127.0.0.1 $P
    
done
