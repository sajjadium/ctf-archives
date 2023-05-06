#!/bin/bash
exec 2>/dev/null
timeout --foreground -k 5 120 ./chal.py

