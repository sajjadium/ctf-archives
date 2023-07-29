#!/bin/sh

qemu-system-x86_64 \
    -kernel bzImage \
    -initrd initramfs.cpio.gz \
    -append "console=ttyS0 quiet loglevel=3 oops=panic" \
    -enable-kvm \
    -monitor /dev/null \
    -nographic \
    -no-reboot

