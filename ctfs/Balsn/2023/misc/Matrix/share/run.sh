#!/bin/bash

exec 2>/dev/null

cd /home/Matrix
timeout 600 python3 chal.py
