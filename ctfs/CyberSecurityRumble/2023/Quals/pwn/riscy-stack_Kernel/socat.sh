#!/bin/sh

socat TCP-LISTEN:4162,reuseaddr,fork,su=chall EXEC:./start.sh,stderr
