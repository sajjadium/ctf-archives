#!/bin/sh
qemu-system-x86_64 \
    -m 128M \
    -cpu kvm64 \
    -kernel bzImage \
    -initrd rootfs.cpio.gz \
    -hdb flag.txt \
    -snapshot \
    -nographic \
    -monitor /dev/null \
    -no-reboot \
    -append "rootwait root=/dev/vda console=ttyS0 kpti=1 quiet panic=1 nokaslr"

