#!/bin/sh

BINARY=/home/user/chall

while :; do
    socat -dd -T60 tcp-l:1337,reuseaddr,fork,keepalive,su=user exec:$BINARY,stderr
done
