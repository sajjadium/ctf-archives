#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4456)
    echo -n 'm' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    M=$(echo -n "$M" | rev | sed 's/5x/2/' | rev)

    P=4463
    if [[ -c /tmp/ping/drop_shot ]] ; then
        rm /tmp/ping/drop_shot
        touch /tmp/ping/smash 
        M="$( echo -en "$M" | head -n -2 )"
        P=$(($P-10))
    fi

    if [[ -w /tmp/pong/serve ]] ; then
        rm /tmp/pong/serve
        touch /tmp/ping/backhand 
        M="$( echo -en "$M" | head -n -2 )"
        P=$(($P+10))
    fi
    

    echo -en "$M" | netcat -N 127.0.0.1 $P
done
