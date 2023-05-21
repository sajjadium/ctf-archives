#!/usr/bin/env bash

while ! test -e /dev/null
do
    sleep 1
done

sleep 5

(while sleep 300;do rm /tmp/* ;done) & 

(while sleep 1;do socat TCP-LISTEN:5000,reuseaddr,fork EXEC:/start_client.sh ;done) &
(while sleep 1;do socat TCP-LISTEN:5001,reuseaddr,fork EXEC:/start_server.sh ;done) 
