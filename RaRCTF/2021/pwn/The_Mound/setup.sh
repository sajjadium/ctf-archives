#!/bin/sh
mv /pwn/flag.txt /pwn/$(xxd -l 16 -p /dev/urandom).txt
service xinetd start
sleep infinity