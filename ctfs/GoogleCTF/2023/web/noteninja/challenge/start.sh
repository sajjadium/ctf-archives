#!/usr/bin/bash
/home/user/cleanup.sh &
while true; do
  PORT=1337 node /home/user/server.js
done
