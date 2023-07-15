#!/bin/sh
s=`dd bs=18 count=1 if=/dev/urandom 2>/dev/null | base64 | tr +/ __`
docker run --rm --name $s -it sharr timeout -s9 300 bash
