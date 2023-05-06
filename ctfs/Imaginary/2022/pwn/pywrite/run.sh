#!/bin/bash

LD_PRELOAD=./libc.so.6 ./ld-2.31.so ./python3 ./vuln.py 2>&1 1>&1
