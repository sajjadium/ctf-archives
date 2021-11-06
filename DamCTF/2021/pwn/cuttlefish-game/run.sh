#!/bin/bash

qemu-system-x86_64 \
    -kernel "bzImage" \
    -m 128 \
    -initrd "initramfs.cpio.gz" \
    -nographic \
    -monitor none \
    -net none \
    -no-reboot \
    -append "console=ttyS0" \
    -cpu kvm64,+smep,+smap
