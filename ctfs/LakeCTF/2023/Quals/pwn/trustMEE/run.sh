#!/bin/sh

/opt/OpenTee/bin/opentee-engine
sleep 1
chmod +r /tmp/open_tee_sock
chmod +w /tmp/open_tee_sock

tail -f /dev/null