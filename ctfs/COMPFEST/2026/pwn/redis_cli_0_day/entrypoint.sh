#!/bin/sh

set -eu

FLAG_PATH=/home/ctf/flag.txt
if [ ! -r "$FLAG_PATH" ]; then
    echo "Flag file is missing or unreadable: $FLAG_PATH" >&2
    exit 1
fi

exec socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"./run.sh",su=ctf
