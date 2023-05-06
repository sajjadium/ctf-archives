#!/bin/bash
rm -rf solve.py
gcc -o /app/yeti /app/yeti.c -g -no-pie -Wl,-z,relro -fstack-protector
pwninit --bin /app/yeti --libc lib/libc-2.27-2.so --ld lib/ld-2.27.so
