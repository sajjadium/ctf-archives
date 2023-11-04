#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4468)
    echo -n 'y' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    N=${M:26:2}


    if [[ -S /proc/self/fd/0 ]] ; then 
        M=${M//'t'/'0'}
    fi 
    
    M=${M:0:26}${M:28}

    for FILE in $(ls /tmp/ping)
    do 
    if [[ "$FILE" =~ ^...$ ]] ; then 
        echo -n "$N" >> "/tmp/ping/$FILE"
    fi
    done
    N=$(awk -F"_" '{print NF-1}' <<< "$(cat /tmp/path)")
    P=$((4386 + $N*22))
    echo -en "$M" | netcat -N 127.0.0.1 $P
done
