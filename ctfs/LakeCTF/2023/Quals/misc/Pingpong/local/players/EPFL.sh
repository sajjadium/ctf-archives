#!/bin/bash
set -e

rm -rf /tmp/ping
rm -rf /tmp/pong
printf "EPFL" > /tmp/path
netcat -N 127.0.0.1 4400 < /tmp/message.txt