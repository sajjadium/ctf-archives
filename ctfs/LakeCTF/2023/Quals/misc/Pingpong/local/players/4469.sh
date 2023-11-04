#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4469)
    echo -n 'z' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -a /tmp/ping/smash ]] ; then 
        rm /tmp/ping/smash
        touch /tmp/pong/smash
    fi

    N="$( echo -en "$M" | tail -c 1 )"
    L=$(cat /tmp/path | wc -m)
    P=$(( ($N*123)%137 - ((($L%5)*29)%32) + 4494))
    M=EPFL${M}

done
