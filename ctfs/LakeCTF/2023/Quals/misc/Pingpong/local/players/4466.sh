#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4466)
    echo -n 'w' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -x /tmp/pong/serve ]] ; then 
        rm /tmp/pong/serve
        touch /tmp/ping/fronthand
        M=${M//'j'/'_'}
    fi 

    if [[ -G /tmp/ping/smash ]] ; then 
        rm /tmp/ping/smash
        touch /tmp/pong/smash
    fi 
    
    N=${M:30:6}
    M=${M:0:30}${M:36}
    if [[ -w "/tmp/pong/$N" && -s "/tmp/pong/$N" ]] ; then 
        touch /tmp/ping/$N
    fi
    P=$(($(echo -n "$N" | sha256sum | head -c 4) + 237))
    echo -en "$M" | netcat -N 127.0.0.1 $P
done
