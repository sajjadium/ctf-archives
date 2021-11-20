#!/bin/sh
exec 2>/dev/null
cd /home/metaeasy
timeout 60 python3 challenge.py
