#!/bin/sh

cd /home/user
timeout --foreground -s 9 60s python3.12 executor.py

