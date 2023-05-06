#!/bin/sh

/usr/bin/qemu-system-x86_64 \
    -m 64M \
    -kernel $PWD/bzImage \
    -initrd $PWD/initramfs.cpio.gz \
    -nographic \
    -monitor none \
    -no-reboot \
    -cpu kvm64,+smep,+smap \
    -append "console=ttyS0 nokaslr quiet"
