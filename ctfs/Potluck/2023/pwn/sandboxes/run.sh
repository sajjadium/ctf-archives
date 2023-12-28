#!/bin/sh

exec qemu-system-x86_64 \
    -enable-kvm \
    -cpu host \
    -smp 2 \
    -device virtio-rng-pci \
    -kernel kernel \
    -initrd initramfs.cpio.gz \
    -nographic \
    -monitor /dev/null \
    -append "console=ttyS0 quiet"
