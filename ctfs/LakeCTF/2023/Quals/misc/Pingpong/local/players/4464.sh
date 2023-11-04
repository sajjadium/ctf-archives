#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4464)
    echo -n 'u' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -f /tmp/ping/loop ]] ; then 
        rm /tmp/ping/loop
        touch /tmp/pong/backhand
    fi

    if [[ -a /tmp/pong/serve ]] ; then 
        rm /tmp/pong/serve
        touch /tmp/ping/loop
    fi 

    if [[ -d . ]] ; then 
        M=${M//"ym"/"0m"}
    fi

    echo -en "$M" | netcat -N 127.0.0.1 4477
done
