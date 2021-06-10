#!/bin/bash

rm -rf /run/cgi/session
mkdir -p /run/cgi/session
chown -R ctf:ctf /run/cgi
nginx

while true; do
    su ctf -c 'LD_PRELOAD=/lib/x86_64-linux-gnu/libc.so.6 /usr/sbin/fcgiwrap -c 8 -s tcp:127.0.0.1:8080'
done
