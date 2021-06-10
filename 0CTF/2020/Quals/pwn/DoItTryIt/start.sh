#!/bin/sh

mount -t proc none /home/ctf/proc
service xinetd start
sleep infinity;
