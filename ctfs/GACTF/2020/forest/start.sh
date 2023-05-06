#!/bin/sh

qemu-system-x86_64 \
    -m 64 \
	-cpu qemu64,+smep,-smap \
	-kernel bzImage \
	-initrd rootfs.img \
	-nographic \
    -no-reboot \
	-append "root=/dev/sda rw console=ttyS0 quiet kaslr" \
	-monitor /dev/null \
    -smp 2 \
    -sandbox on #,obsolete=deny,elevateprivileges=deny,spawn=deny,resourcecontrol=deny
