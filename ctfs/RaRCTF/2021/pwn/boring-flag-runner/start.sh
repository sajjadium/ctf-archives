#!/bin/sh

cd /challenge
FILENAME=$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 16)
python3 getprog.py /tmp/$FILENAME
timeout 10 ./boring-flag-checker /tmp/$FILENAME > /dev/null
rm /tmp/$FILENAME
