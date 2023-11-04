#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4467)
    N=$(awk -F"_" '{print NF-1}' <<< "$(cat /tmp/path)")

    echo -n 'x' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -a /tmp/ping/short ]] ; then 
        rm /tmp/ping/short
        touch /tmp/pong/short
    fi

    if [[ -e /tmp/pong/serve ]] ; then
        rm /tmp/pong/serve
        touch /tmp/ping/drop_shot
    fi  
    
    P=$((1111*$N+1))
    echo -en "$M" | netcat -N 127.0.0.1 $P
done
