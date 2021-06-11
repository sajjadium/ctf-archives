#!/bin/sh

cd /home/nutty
timeout --foreground 300 qemu-system-x86_64 \
	-m 128 \
	-kernel bzImage \
	-nographic \
        -smp 1 \
        -cpu kvm64,+smep,+smap \
	-append "console=ttyS0 quiet kaslr" \
        -initrd initramfs.cpio \
	-monitor /dev/null \
