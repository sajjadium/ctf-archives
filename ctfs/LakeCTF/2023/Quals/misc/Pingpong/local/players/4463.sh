#!/bin/bash
set -e

while :
do
    M=$(netcat -l 4463)
    echo -n 't' >> /tmp/path
    if ! [[ -d /tmp/ping && -d /tmp/pong ]] ; then 
        M=^$M
    fi
    
done
