#!/bin/sh
cd /home/user
python3 -m waitress --host 0.0.0.0 --port 1337 --no-expose-tracebacks "chal:app"
