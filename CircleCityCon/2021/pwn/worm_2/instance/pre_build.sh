#!/usr/bin/env bash

set -eu

max_depth=$1

for d in $(seq 1 $max_depth)
do
    addgroup user$d
    useradd -M -g user$d -s /bin/bash user$d
done

mkdir /keys

for d in $(seq 2 $max_depth)
do
    echo "[*] Compiling key $d ..."
    gcc -o /keys/key$d -DID=$(id -u user$d) /key.c &> /dev/null
    echo "[*] Done"
done
