#!/bin/bash
qemu-system-x86_64 \
    -m 128M \
    -kernel bzImage \
    -initrd rootfs.cpio \
    -append 'console=ttyS0 kaslr quiet' \
    -monitor /dev/null \
    -cpu kvm64,+smep,+smap \
    -smp cores=1,threads=1 \
    -nographic
