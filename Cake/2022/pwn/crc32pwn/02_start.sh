#!/bin/sh
s=`dd bs=18 count=1 if=/dev/urandom 2>/dev/null | base64 | tr +/ _.`
docker run --rm --name $s -it crc32pwn timeout -s9 300 bash
