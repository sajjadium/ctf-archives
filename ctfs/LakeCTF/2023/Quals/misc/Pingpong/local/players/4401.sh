#!/bin/bash
set -e

M=$(netcat -l 4401)
if [[ ! -f /tmp/path ]] ; then
    exit 4
fi
printf '}' >> /tmp/path

if ! [[ -d /tmp/ping && -d /tmp/pong && -z $( diff -r /tmp/ping /tmp/pong ) ]] ; then 
    M=^$M
fi

if [[ "$M" == *"^"* ]] ; then 
    exit 55
fi 

if [[ "$M" == "$( cat /tmp/path )" && $( cat /tmp/path | wc -m ) -lt 60 && $( cat /tmp/path | wc -m ) -gt 40 ]] ; then 
    echo "SUCCESS"
    if [[ -f flag.txt ]] ; then
        cat flag.txt
    else 
        cat /tmp/path
    fi
else 
    echo "FAIL"
fi
