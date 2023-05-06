#!/bin/sh
qemu-system-x86_64 \
    -m 64M \
    -kernel ./bzImage \
    -initrd ./rootfs.cpio \
    -append "console=ttyS0 oops=panic panic=1 kpti=1 kaslr quiet" \
    -cpu kvm64,+smep \
    -monitor /dev/null \
    -nographic
