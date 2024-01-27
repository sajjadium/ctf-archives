#!/bin/sh


echo /app/flag.c
gcc /app/flag.c -o /flag
chmod 111 /flag

rm /app/flag.c

/usr/bin/supervisord -c /etc/supervisord.conf
