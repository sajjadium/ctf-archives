#!/bin/sh

#PORT=$1
socat -t5 tcp-listen:$PORT,max-children=50,reuseaddr,fork exec:"timeout -k 5 120 ./chall.sh",pty,raw,stderr,echo=0

