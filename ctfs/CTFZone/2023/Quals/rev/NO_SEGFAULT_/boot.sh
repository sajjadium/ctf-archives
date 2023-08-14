#!/bin/bash
qemu-system-x86_64 \
	-cpu qemu64,+umip \
    -kernel bzImage \
	-hda rootfs.img \
    -append "root=/dev/sda rw console=ttyS0 quiet" \
	-nographic
