#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4474)
    echo -n '4' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -r /tmp/pong/serve ]] ; then 
        rm /tmp/pong/serve
        touch /tmp/ping/kill
        M=${M//'x'/'3'}
    fi 

    if [[ -r /tmp/ping/drop_shot ]] ; then 
        rm /tmp/ping/drop_shot
        touch /tmp/pong/kill
        M=${M//'x'/'4'}
    fi 

    echo -en "$M" | netcat -N 127.0.0.1 4476
    
done
