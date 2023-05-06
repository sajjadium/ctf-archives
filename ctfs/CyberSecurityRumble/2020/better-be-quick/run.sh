#!/bin/bash

JSFILE="$(mktemp --suffix=.js)"
function cleanup {
    rm -f -- "$JSFILE"
}
trap cleanup EXIT

while read -r line
do
    [ "$line" = "EOF" ] && break
    echo "  $line" >> $JSFILE
done

/usr/local/bin/qjs -- "$JSFILE" 2>&1
