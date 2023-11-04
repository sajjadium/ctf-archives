#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4444)
    echo -n 'a' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    
    if [[ "$M" == *Voila ]] ; then 

        echo -en "$M" >> /tmp/pong/lob
        echo -en "success" >> /tmp/pong/winner
        echo -en "0" >> /tmp/pong/score

        touch /tmp/ping/serve

        M="$( echo -en "$M" | head -n -2 )"
    fi 

    L="$(echo -n "$M"| wc -l)"
    P=$((159*$L+23))
    echo -en "$M" | netcat -N 127.0.0.1 $P

done
