#!/bin/sh

KEY=$(head -c 16 /dev/urandom | base64 -w0)
gunicorn --chdir /app "app:load_app(\"$KEY\")" -w 4 --threads 4 -b 0.0.0.0:1337
