#!/bin/bash

sudo qemu-system-x86_64 \
    -m 1024M \
    -kernel bzImage \
    -initrd rootfs.img \
    -monitor /dev/null \
    -append "root=/dev/ram console=ttyS0 oops=panic panic=1 kpti=1 quiet" \
    -cpu kvm64,+smep,+smap \
    -smp cores=2,threads=2 \
    -nographic -enable-kvm
