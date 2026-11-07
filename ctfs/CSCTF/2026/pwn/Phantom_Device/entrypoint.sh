#!/bin/sh
# Runtime flag injection — CTF infrastructure sets FLAG env var
if [ -n "$FLAG" ]; then
    printf '%s\n' "$FLAG" > /flag.txt
fi
chmod 0444 /flag.txt 2>/dev/null
exec socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"/challenge/handler.sh",stderr,setsid
