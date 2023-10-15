#!/bin/sh

PORT=${1:-1337}
exec ./ynetd -u nobody -d /chall -p ${PORT} -t 120 -lt 120 -lpid 32 -lm -1 /chall/run_chall.sh
