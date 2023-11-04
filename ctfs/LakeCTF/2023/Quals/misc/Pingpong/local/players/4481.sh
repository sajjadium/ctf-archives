#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4481)
    if [[ $(cat /tmp/path) =~ "-" ]] ; then 
        M=^$M
    fi
    echo -n '-' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    P=4400
    if [[ -a /tmp/ping/serve ]] ; then 
        P=4460
        touch /tmp/pong/serve
    fi 
    if [[ -e /tmp/pong/serve ]] ; then 
        P=4458
        touch /tmp/pong/serve
    fi

    if [[ -G /tmp/ping/serve ]] ; then 
        P=4459
        rm /tmp/ping/serve

    fi 
    touch /tmp/pong/dead_ball
    
    M=$( echo -en "$M" | head -n -3 )
    M=${M:0:15}-${M:15}
    echo -en "$M" | netcat -N 127.0.0.1 $P
done
