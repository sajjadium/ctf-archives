#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4458)
    echo -n 'o' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    ACT=false

    if [[ -e /tmp/ping/loop ]] ; then 
        ACT=true
        rm /tmp/ping/loop
        touch /tmp/pong/flat
    fi 

    if [[ -e /tmp/pong/cross_court ]] ; then 
        ACT=true
        rm /tmp/pong/cross_court 
        touch /tmp/ping/dead_ball
    fi

    M="$( echo -en "$M" | head -n -1 )"

    if $ACT ; then 
        M="${M//'f'/'W'}"
    fi

    echo -en "$M" | netcat -N 127.0.0.1 4461
done
