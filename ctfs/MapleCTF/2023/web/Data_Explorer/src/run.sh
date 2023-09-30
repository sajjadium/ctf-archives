#!/bin/bash
export FLAG=$(cat flag.txt) PYTHONOPTIMIZE=1
exec gunicorn --bind 0.0.0.0 -w 1 server:app
