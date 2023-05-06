#!/bin/bash -u

JSFILE="$(mktemp --suffix=.js)"
function cleanup {
    rm -rf -- "$JSFILE"
    rm -rf -- "/home/ctf$JSFILE"
}
trap cleanup EXIT

cat > "$JSFILE"

cp "$JSFILE" "/home/ctf$JSFILE"
chmod 644 "/home/ctf$JSFILE"
/usr/sbin/chroot --userspec=1000:1000 /home/ctf timeout 600 ./ch "$JSFILE" 2>&1
