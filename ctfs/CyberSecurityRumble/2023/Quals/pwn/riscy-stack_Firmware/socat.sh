#!/bin/sh

socat TCP-LISTEN:4163,reuseaddr,fork,su=chall EXEC:./start.sh,stderr
