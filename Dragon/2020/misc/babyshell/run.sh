#!/bin/sh

exec python2 pow.py 25 30 \
qemu-system-x86_64  -kernel vmlinuz-lts  -initrd initramfs.img.lz4  -nographic -monitor /dev/null    -append "console=ttyS0 quiet"
