#!/bin/sh

set -eu

PWD="`pwd`"

if swapon -s 2>&1 | grep -q '.'; then
    echo "You should turn the swap off"
    exit 1
fi

~/nsjail/nsjail -Q -Ml --port 1337 -R "$PWD/main:/main" -R "$PWD/flag.txt:/flag.txt" -R /dev/urandom -T /tmp --cgroup_mem_max 170000384 -- /main
