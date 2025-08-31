#!/bin/sh
qemu-system-x86_64 \
    -s \
    -m 512 \
    -smp 1 \
    -nographic \
    -kernel "bzImage" \
    -append "console=ttyS0 loglevel=7 panic=-1" \
    -no-reboot \
    -cpu host \
    -initrd "./initramfs.cpio.gz" \
    -monitor /dev/null \
    -enable-kvm
