#!/bin/sh

cd /home/user
GLOG_minloglevel=3 timeout --foreground -s 9 60s stdbuf -i0 -o0 -e0 ./sloader ./chall
