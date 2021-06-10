#!/bin/bash

qemu-system-x86_64 \
	-enable-kvm \
        -cpu kvm64 \
	-m 128 \
	-kernel bzImage \
	-nographic \
	-append "console=ttyS0 init=/init quiet" \
	-initrd rootfs.img \
	-monitor /dev/null
