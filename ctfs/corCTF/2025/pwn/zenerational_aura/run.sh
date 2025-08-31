#!/bin/sh
qemu-system-x86_64 \
    -m 2G \
    -s \
    -smp 1 \
    -nographic \
    -kernel "bzImage" \
    -append "console=ttyS0 panic=-1 oops=panic pti=off" \
    -no-reboot \
    -cpu host \
    -initrd "./initramfs.cpio.gz" \
    -monitor /dev/null \
    -enable-kvm
