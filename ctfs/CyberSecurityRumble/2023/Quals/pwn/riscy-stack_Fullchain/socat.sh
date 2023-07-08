#!/bin/sh

socat TCP-LISTEN:4164,reuseaddr,fork,su=chall EXEC:./start.sh,stderr
