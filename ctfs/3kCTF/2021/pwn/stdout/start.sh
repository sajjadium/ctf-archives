#!/bin/sh

mv /home/ctf/flag.txt /home/ctf/$(head -c 500 /dev/urandom | sha512sum | cut -d " " -f1).txt
/etc/init.d/xinetd start;
sleep infinity;
