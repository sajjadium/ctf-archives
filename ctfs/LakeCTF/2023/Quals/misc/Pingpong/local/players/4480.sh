#!/bin/bash
set -e

iter=0
while :
do
    M=$(netcat -l 4480)
    iter=$((iter+1))

    L=$(cat /tmp/path | wc -m)
    echo -n '_' >> /tmp/path

    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ $M == *'_'* ]] ; then 
        exit 5
    fi

    M=$( echo -e "$M" | tr "0-9A-Za-z}" "1-9A-Za-z^" )

    if [[ $iter -gt 5 ]] ; then
        TRACE="$(cat /tmp/path)"
        for ((I=0;I<${#TRACE};I++))
        do
            C=${TRACE:$I:1}
            if [[ $C == '_' ]] ; then 
                M=${M:0:I}_${M:I}
            fi 
        done
    fi

    if [[ -a /tmp/ping/smash ]] || [[ -e /tmp/ping/kill ]] ; then 
        rm -f /tmp/ping/smash /tmp/ping/kill
        echo "$(($(cat /tmp/ping/score) + 1))" > /tmp/ping/score
        touch /tmp/ping/serve
    else
        if [[ -r /tmp/pong/smash ]] || [[ -f /tmp/pong/kill ]] ; then
            rm -f /tmp/pong/smash /tmp/pong/kill
            echo "$(($(cat /tmp/pong/score) + 1))" > /tmp/pong/score
            touch /tmp/pong/serve
        fi
    fi 
    

    P=-1
    if [[ $L -lt 31 ]] ; then
        P=$((($L*13)%33 + 4441))
    else 
        P=$((($L*36)%59 + 4399))
    fi
    echo -en "$M" | netcat -N 127.0.0.1 "$P"
done

