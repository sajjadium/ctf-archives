#! /usr/bin/env bash

if [ -d ./src ]; then
    echo "[*] rm -r ./src"
    rm -r ./src
fi

echo "[*] docker-compose down"
docker-compose down