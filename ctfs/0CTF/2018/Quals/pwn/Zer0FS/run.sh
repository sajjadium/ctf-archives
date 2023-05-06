#!/bin/sh

stty intr ^]

qemu-system-x86_64 -enable-kvm -cpu kvm64,+smep,+smap -m 64M -kernel ./bzImage -initrd ./rootfs.cpio -append "root=/dev/ram rw console=ttyS0 oops=panic panic=1 quiet kaslr" -monitor /dev/null -nographic 2>/dev/null
