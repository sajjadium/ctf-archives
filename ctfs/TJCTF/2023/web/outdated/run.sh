#!/bin/bash

mkdir uploads && mv flag.txt flag-$(cat /proc/sys/kernel/random/uuid).txt
exec gunicorn -b 0.0.0.0:5000 -w 4 app:app
