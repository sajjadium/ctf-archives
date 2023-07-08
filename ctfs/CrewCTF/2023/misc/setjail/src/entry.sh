#!/bin/sh

socat - 'system:stty -echo; python3 main.py,pty'
kill -KILL 0
