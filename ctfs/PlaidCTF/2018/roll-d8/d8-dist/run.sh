#!/bin/sh
# Approximation of the server-side command.
./d8 --max-semi-space-size=4096 --max-old-space-size=8192 test.js >/dev/null 2>/dev/null
echo $?
