#!/bin/bash
#
timeout --foreground 28800 /usr/bin/qemu-system-x86_64 \
	-m 256M\
	-kernel ./bzImage\
	-initrd ./initramfs.cpio.gz \
	-nographic \
	-monitor none \
	-no-reboot \
	-append "console=ttyS0 kaslr nosmap nosmep nokpti quiet panic=0"\
	-smp 2

