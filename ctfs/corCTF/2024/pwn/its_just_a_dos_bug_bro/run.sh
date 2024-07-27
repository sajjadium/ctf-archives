#!/bin/sh
qemu-system-x86_64 \
    -s \
    -m 512 \
    -smp 1 \
    -nographic \
    -kernel "bzImage" \
    -append "console=ttyS0 loglevel=3 panic=-1 oops=panic clearcpuid=smap pti=on no5lvl" \
    -no-reboot \
    -netdev user,id=net \
    -cpu host \
    -initrd "./initramfs.cpio.gz" \
    -enable-kvm
