#!/bin/bash

exec timeout 300 qemu-system-x86_64 \
    -m 128M \
    -nographic \
    -kernel ./bzImage \
    -append 'console=ttyS0 oops=panic panic=1 quiet loglevel=3 kaslr' \
    -monitor /dev/null \
    -initrd ./rootfs.cpio.gz  \
    -smp cores=2,threads=2 \
    -cpu kvm64,smep,smap \
    -no-reboot
