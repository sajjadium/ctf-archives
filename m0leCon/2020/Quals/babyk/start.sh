#!/bin/bash

random_string=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
real_hash=$(echo -n $random_string | md5sum | cut -d" " -f1)

echo "MD5 for $random_string if you may! "
read -t 15 computed_hash

if [ $? -ne 0 ] || [ $real_hash != $computed_hash ]; then
	echo "NOPE"
	exit 1
else
timeout --foreground 300 qemu-system-x86_64 \
	-m 64M \
	-kernel /home/pwn/bzImage \
	-nographic \
	-append "root=/dev/ram rw oops=panic panic=1 console=ttyS0 quiet nokaslr" \
	-initrd /home/pwn/initramfs.cpio \
	-monitor /dev/null
fi