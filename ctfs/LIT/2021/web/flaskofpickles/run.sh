#!/bin/bash

cd /flaskofpickles
python3 -m gunicorn --worker-tmp-dir /dev/shm --bind 0.0.0.0:1337 flaskofpickles:app

