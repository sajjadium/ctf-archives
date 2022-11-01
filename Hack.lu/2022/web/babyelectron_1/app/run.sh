#!/usr/bin/env bash
rm -rf /tmp/.X99-lock
Xvfb :99 &

# start bot
timeout -s 2 5 ./node_modules/.bin/electron . --disable-gpu --no-sandbox
sleep 15
