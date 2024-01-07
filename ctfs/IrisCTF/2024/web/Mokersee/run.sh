#!/bin/sh
cd /home/user
python3 -m gunicorn -w 8 -b 0.0.0.0:1337 --timeout 10 "chal:app"
