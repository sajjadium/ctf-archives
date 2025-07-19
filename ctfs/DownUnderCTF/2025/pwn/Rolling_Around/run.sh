#!/bin/sh

qemu-system-x86_64 \
    -m 256M \
    -kernel $PWD/bzImage \
    -initrd $PWD/initramfs.cpio.gz \
    -nographic \
    -monitor none \
    -no-reboot \
    -cpu kvm64,+smep,+smap \
    -append "console=ttyS0 quiet"  
