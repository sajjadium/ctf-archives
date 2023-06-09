#!/bin/bash
socat -v tcp-listen:1337,reuseaddr EXEC:'stdbuf -i0 -o0 -e0 python3 visit.py'
