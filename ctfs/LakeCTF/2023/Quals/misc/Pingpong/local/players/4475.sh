#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4475)
    echo -n '5' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    
    if [[ -r /tmp/ping/serve ]] ; then
        M="$( echo -en "$M" | head -n -1 )"
        M=z${M}
        rm /tmp/ping/serve
        touch /tmp/pong/loop
        echo -en "$M" | netcat -N 127.0.0.1 4451
    else 
        echo -en "$M" | netcat -N 127.0.0.1 4457
    fi
done
