#!/bin/sh

export LD_PRELOAD=/challenge/preload.so

chroot --userspec=1000:1000 /chroot \
    /bin/python3.11 -u /challenge/balloon.py
