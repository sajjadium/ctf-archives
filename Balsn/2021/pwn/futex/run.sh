#!/bin/bash

exec qemu-system-x86_64 \
    -m 128M \
    -nographic \
    -kernel ./bzImage \
    -append 'console=ttyS0 loglevel=3 oops=panic panic=1' \
    -initrd ./initramfs.cpio.gz \
    -smp cores=2,threads=2 \
    -drive file=./flag,format=raw,if=virtio,readonly \
    -monitor none

