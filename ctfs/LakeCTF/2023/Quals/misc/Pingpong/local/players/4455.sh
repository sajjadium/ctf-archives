#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4455)
    echo -n 'l' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -s /tmp/pong/serve ]] ; then 
        rm /tmp/pong/serve
        touch /tmp/ping/kill
    fi

    if [[ -a /tmp/pong/flat ]] ; then 
        rm /tmp/pong/flat
        touch /tmp/ping/dead
    fi 

    if [[ $(echo -ne "$M" | wc -l) -eq 1 ]] ; then 
        M=$( echo -en "$M" | tr -d '\n' )
        if [[ $M == *bracket ]] ; then 
            M=${M::-7}}
        fi
        echo -en "$M" | netcat -N 127.0.0.1 4474

    else
        echo -en "$M" | netcat -N 127.0.0.1 4447
    fi
    
done
