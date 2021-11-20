#!/bin/bash

exec 2>/dev/null

qemu-system-x86_64 \
	-m 256 \
	-cpu kvm64,+smep,+smap \
	-kernel /home/ElfFortress/bzImage \
	-initrd /home/ElfFortress/initramfs.cpio \
	-nographic \
	-append "console=ttyS0 kaslr quiet"
