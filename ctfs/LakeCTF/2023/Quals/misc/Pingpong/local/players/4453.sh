#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4453)
    echo -n 'j' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -r /tmp/pong/dead ]] ; then 
        rm /tmp/pong/dead
        touch /tmp/ping/serve
    fi 

    M=${M//'a'/'9'}

    echo -en "$M" | netcat -N 127.0.0.1 4445
    
done
