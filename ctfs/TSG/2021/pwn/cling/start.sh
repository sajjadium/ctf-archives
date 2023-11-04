#!/bin/sh

cat /home/user/chall.c - | timeout --foreground -s 9 300s /cling/bin/cling --nologo
