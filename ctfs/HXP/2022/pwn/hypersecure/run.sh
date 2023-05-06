#!/bin/sh

qemu-system-x86_64 \
	-cpu qemu64,+smep,+smap,+svm \
	-kernel ./bzImage \
	-initrd ./initramfs.cpio \
	-m 256 \
	-append "console=ttyS0 kaslr oops=panic ip=dhcp root=/dev/ram rdinit=/init quiet" \
	-nographic \
	-monitor /dev/null \
	-snapshot \
	-smp 1 \
	-no-reboot
