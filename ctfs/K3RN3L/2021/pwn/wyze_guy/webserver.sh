#!/bin/bash
echo 0 > /proc/sys/kernel/randomize_va_space
mkdir -p /tmp/www/SDPath
while true
do
	cd /home/user && python2 /home/user/webserver.py
done

