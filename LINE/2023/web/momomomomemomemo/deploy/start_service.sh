#! /usr/bin/env bash

if [ -d ./src ]; then
    echo "[*] rm -r ./src"
    rm -r ./src
fi

echo "[*] cp -r ../src ."
cp -r ../src . 

echo "[*] docker-compose build && docker-compose up -d"
docker-compose build && docker-compose up -d