#!/bin/sh
# Add your startup script

while true;
do
    port=9999
    pid=$(netstat -nlp | grep :$port | awk '{print $7}' | awk -F"/" '{ print $1 }');

    if [  -n  "$pid"  ];  then
        kill  -9  $pid;
    fi
    timeout -k 1 60 ./dns -C ./dns.conf 2>/dev/null

    sleep 15
done
