#!/bin/sh

socat TCP-LISTEN:4141,reuseaddr,fork,su=chall EXEC:"./start.sh",stderr
