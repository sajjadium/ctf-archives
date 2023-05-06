#!/bin/env sh

qemu-system-x86_64 -kernel bzImage       \
    -initrd initramfs.cpio.gz -nographic \
    -append "console=ttyS0"

