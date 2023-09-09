#!/bin/sh
for i in $(seq 1 8); do
    export PYTHONHASHSEED="$(python3 -c 'import secrets;print(secrets.randbelow(2**32))')"
    ./server.py
    [ $? -ne 87 ] && exit
done
echo "${FLAG:-NO_FLAG_FOUND}"
