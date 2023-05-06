#!/bin/bash

nginx -g "daemon off;" &

su ctf

python3 app.py
