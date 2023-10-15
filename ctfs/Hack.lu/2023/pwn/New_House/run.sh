#!/bin/sh

PORT=${1:-1337}
exec ./ynetd -u nobody -d /chall -p ${PORT} -t 120 -lt 120 -lpid 16 -lm 20000000 /chall/new_house
