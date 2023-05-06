#!/bin/bash

qemu-system-x86_64 \
    -smp 2 \
    -kernel ./bzImage \
    -initrd ./rootfs.cpio.gz \
    -nographic \
    -append "console=ttyS0 quiet oops=panic panic=1 nokaslr" \
    -monitor /dev/null \
    -no-reboot \
