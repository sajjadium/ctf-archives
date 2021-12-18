#!/bin/sh

exec qemu-system-x86_64 \
	-cpu kvm64,+smep,+smap \
	-kernel ./bzImage \
	-initrd ./initramfs.cpio \
	-m 128 \
	-append "console=ttyS0 kaslr oops=panic ip=dhcp root=/dev/ram rdinit=/init" \
	-nographic \
	-monitor /dev/null \
	-snapshot \
	-no-reboot \
	-smp 1 \
	-hdb flag.txt
