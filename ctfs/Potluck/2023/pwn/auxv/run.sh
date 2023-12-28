#!/bin/sh

set -e

qemu-system-x86_64 \
     -initrd prebuilt_system/initramfs.cpio.gz \
     -kernel prebuilt_system/bzImage \
     -append "root=/dev/ram console=ttyS0 oops=panic quiet" \
     -nographic \
     -monitor /dev/null \
     -m 256 \
     -smp 1 \
     -no-reboot
