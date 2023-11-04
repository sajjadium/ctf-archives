#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4449)
    echo -n 'f' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi

    if [[ -O /tmp/ping/drop_shot ]] ; then 
        rm /tmp/ping/drop_shot
        touch /tmp/pong/flat
        M=${M/"-p1"/"-p0"}
    fi

    if [[ /tmp/ping/drop_shot -nt /tmp/pong/serve ]] ; then 
        rm /tmp/pong/serve
        touch /tmp/ping/drop_shot
        M=${M/"1n"/"0n"}
    fi

    echo -en "$M" | netcat -N 127.0.0.1 4455
done
