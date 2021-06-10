#!/bin/bash

qemu-system-x86_64 \
    -smp 1 -m 100M \
    -kernel vmlinuz \
    -append "console=ttyS0 quiet ip=dhcp" \
    -initrd initramfs.cpio.gz \
    -fda flag.txt \
    -snapshot \
    -nographic \
    -monitor /dev/null \
    -no-reboot

