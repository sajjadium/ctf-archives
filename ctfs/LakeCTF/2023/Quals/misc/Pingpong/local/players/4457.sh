#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4457)
    L=$(cat /tmp/path | wc -c )
    N=$(awk -F"_" '{print NF-1}' <<< "$(cat /tmp/path)")
    echo -n 'n' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -O /tmp/pong/cross_court ]] ; then 
        rm /tmp/pong/cross_court
        touch /tmp/ping/flat
    fi 

    if [[ -r /tmp/ping/loop ]] ; then 
        rm /tmp/ping/loop 
        touch /tmp/pong/backhand
    fi 
    
    if [[ -a /tmp/pong/serve ]] ; then 
        rm /tmp/pong/serve
        touch /tmp/ping/loop
    fi 

    if [[ -a /tmp/ping/short ]] ; then
        rm /tmp/ping/short
        touch /tmp/pong/smash
        M="$( echo -en "$M" | head -n 3 )"
    fi

    M="$( echo -en "$M" | head -n -2 )"

    P=$(( ($N*108)%137 - ((($L%5)*29)%32) + 4394))
    echo -en "$M" | netcat -N 127.0.0.1 $P
done
