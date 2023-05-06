#!/bin/sh
cd /home/pycry
exec timeout -s 9 120 env -i PYTHONHOME=pylib ./python -u run.py
