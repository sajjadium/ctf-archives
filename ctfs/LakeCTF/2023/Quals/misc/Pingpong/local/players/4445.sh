#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4445)
    echo -n 'b' >> /tmp/path
    
    if ! [[ -d /tmp/ping || -d /tmp/pong ]] ; then 
        mkdir /tmp/ping
        mkdir /tmp/pong
        echo -en "1" >> /tmp/ping/score
    else
        rm -rf /tmp/pong
    fi

    C=${M:0:1}
    P=$((4321 + $(printf '%d' "'$C")))
    echo -en "$M" | netcat -N 127.0.0.1 $P

done
