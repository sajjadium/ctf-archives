#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4476)
    echo -n '6' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi


    R=false
    L=$(wc -l <<< ${M})
    P=$(($L%2 + 4480))
    
    if [[ -e /tmp/ping/flat ]] ; then 
        rm /tmp/ping/flat
        touch /tmp/pong/kill
    fi 

    if [[ -a /tmp/ping/kill ]] ; then 
        rm /tmp/ping/kill
        touch /tmp/pong/dead
    fi 


    for FILE in /tmp/ping/*
    do 
        if [[ -h $FILE ]] ; then 
            R=true
            break
        fi
    done

    if $R && [[ -s /tmp/ping/winner ]] ; then 
        echo -en "$M" | netcat -N 127.0.0.1 4401
    else
        echo -en "$M" | netcat -N 127.0.0.1 $P
    fi
    
done
