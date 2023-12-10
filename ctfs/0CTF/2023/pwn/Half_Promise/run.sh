#!/bin/bash -u

lscpu -e
free -h

timeout 180 python3 -u /pow.py

if [ $? -ne 0 ]; then
    echo 'pow failed!'
    exit 1
fi

JSFILE="$(mktemp -p /scripts --suffix=.js)"
function cleanup {
    rm -f "/home/ctf$JSFILE"
}
trap cleanup EXIT

timeout 60 python3 -u /read.py $JSFILE

cp "$JSFILE" "/home/ctf$JSFILE"
chmod 644 "/home/ctf$JSFILE"
/usr/sbin/chroot --userspec=ctf:ctf /home/ctf timeout 240 ./d8 "$JSFILE" 2>&1
