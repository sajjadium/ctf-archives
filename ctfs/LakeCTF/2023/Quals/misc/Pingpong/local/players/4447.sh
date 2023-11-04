#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4447)
    echo -n 'd' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    
    for FILE in $(ls /tmp/ping)
    do 
        if [[ "$FILE" =~ ^...$ ]] ; then 
            if [[ -w /tmp/ping/winner ]] ; then 
                cat "/tmp/ping/$FILE" >> /tmp/ping/winner
            fi 
            rm "/tmp/ping/$FILE"
    fi
    done


    if [[ -c /dev/stdin ]] || [[ /dev/stdin -ef /proc/self/fd/0 ]] ; then 
        M=M$M
    fi


    if [[ -a /tmp/pong/backhand ]] ; then 
        rm /tmp/pong/backhand
        touch /tmp/ping/drop_shot
    fi
    
    N=${M:8:3}
    M=${M:0:8}${M:11}
    

    if [[ -f "/tmp/pong/$N" && ! -a "/tmp/ping/$N" ]] ; then 
        ln -s "/tmp/pong/$N" "/tmp/ping/$N"
    else 
        echo "loop" > "/tmp/ping/$N"
    fi 

    echo -en "$M" | netcat -N 127.0.0.1 4480

done
