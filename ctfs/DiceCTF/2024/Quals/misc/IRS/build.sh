#!/bin/sh
gcc $(python3.12-config --cflags --ldflags --embed) irs.c -o irs
