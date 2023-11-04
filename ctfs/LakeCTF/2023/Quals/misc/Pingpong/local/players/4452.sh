#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4452)
    echo -n 'i' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -w /tmp/ping/serve ]] ; then 
        rm /tmp/ping/serve
        touch /tmp/pong/backhand
        M="$( echo -en "$M" | head -n -1 )"
    fi

    if [[ -L /tmp/pong/dead ]] ; then 
        rm /tmp/pong/dead
        touch /tmp/ping/flat
        M="$( echo -en "$M" | head -n -1 )"
    fi 

    echo -en "$M" | netcat -N 127.0.0.1 4473
done
