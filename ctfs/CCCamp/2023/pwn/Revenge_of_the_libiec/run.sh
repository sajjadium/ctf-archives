#!/bin/bash


(while true; do 
    /home/ctf/libiec61850/build/examples/mms_utility/mms_utility -p 1337 -d -i -f -m
    sleep 1
done) &

dropbear -FBREkwp 1024