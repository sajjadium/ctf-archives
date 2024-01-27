#!/bin/sh

qemu-system-arm -m 512 -M virt,highmem=off \
	-kernel zImage \
        -initrd rootfs.cpio \
	-net nic \
	-net user,hostfwd=tcp::443-:443 \
	-nographic \
	-monitor null
