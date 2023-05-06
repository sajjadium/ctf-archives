#!/bin/sh
qemu-system-x86_64 \
    -m 256M \
    -kernel ./bzImage \
    -initrd ./rootfs.cpio \
    -append "root=/dev/ram rw console=ttyS0 oops=panic panic=1 kaslr pti=off quiet" \
    -cpu qemu64,+smep \
    -monitor /dev/null \
    -nographic
