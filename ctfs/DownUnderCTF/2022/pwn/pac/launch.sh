#!/bin/bash

/usr/bin/qemu-system-x86_64 \
	-m 64M \
	-kernel $PWD/bzImage \
	-initrd $PWD/initramfs.cpio.gz \
	-nographic \
	-monitor none \
	-no-reboot \
	-append "console=ttyS0 kaslr panic=1"
