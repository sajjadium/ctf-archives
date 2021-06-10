#!/bin/sh
./qemu-system-x86_64 \
    -kernel /vmlinuz-4.8.0-52-generic  \
    -append "console=ttyS0 root=/dev/ram oops=panic panic=1 quiet"  \
    -initrd /rootfs.cpio  \
    -m 2G -nographic \
    -L /pc-bios -smp 1 \
    -device denc
