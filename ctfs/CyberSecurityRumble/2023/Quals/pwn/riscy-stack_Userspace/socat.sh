#!/bin/sh

socat TCP-LISTEN:4161,reuseaddr,fork,su=chall EXEC:./start.sh,stderr
