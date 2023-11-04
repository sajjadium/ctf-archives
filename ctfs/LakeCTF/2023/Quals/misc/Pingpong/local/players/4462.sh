#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4462)
    L=$(cat /tmp/path | wc -c )
    N=$(awk -F"_" '{print NF-1}' <<< "$(cat /tmp/path)")
    echo -n 's' >> /tmp/path

    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -f /tmp/ping/winner ]] ; then 
        echo -n "sss" >> /tmp/ping/winner
    else 
        echo -n "sss" >> /tmp/pong/winner
    fi 

    if [[ -a /tmp/ping/cross_court ]] ; then 
        rm /tmp/ping/cross_court
        touch /tmp/pong/backhand
    fi

    if [[ -p /tmp/ping/backhand ]] ; then 
        rm /tmp/ping/backhand
        touch /tmp/pong/dead
    fi

    P=$(( ($N*23)%33 - ((($L%4)*12)%14) + 4440))
    echo -en "$M" | netcat -N 127.0.0.1 $P
done
