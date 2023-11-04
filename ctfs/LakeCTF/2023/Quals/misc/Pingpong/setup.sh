#!/bin/bash
set -e
echo -n "Please put your message.txt in base64:"
read -r B64
echo -n "$B64" | base64 -d -w 0 -i > /tmp/message.txt || exit -1
cat /tmp/message.txt
bash players/run.sh