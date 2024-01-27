#!/bin/bash

rm -rf /tmp/.X99-lock
Xvfb :99 &
cd "/app/app"
#
timeout -k 2 3 node_modules/.bin/electron . --disable-gpu --no-sandbox --args  --ignore-certificate-errors &
