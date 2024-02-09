#!/bin/sh

while true; do
    socat TCP-LISTEN:1337,reuseaddr,fork SYSTEM:'python3 challenge.py'
done
