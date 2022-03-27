#!/bin/bash

# https://georgik.rocks/how-to-start-d-bus-in-docker-container/
# avoids a puppeteer Chrome startup error in some environments like Google Cloud Run
mkdir -p /var/run/dbus
dbus-daemon --config-file=/usr/share/dbus-1/system.conf --print-address&

node /ctf/app/server.js