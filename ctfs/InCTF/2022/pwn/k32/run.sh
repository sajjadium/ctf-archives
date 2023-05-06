#!/bin/sh
qemu-system-x86_64 \
    -m 64M \
    -cpu kvm64,+smep,+smap \
    -kernel bzImage \
    -initrd rootfs.cpio \
    -snapshot \
    -nographic \
    -monitor /dev/null \
    -no-reboot \
    -append "console=ttyS0 kaslr kpti=1 quiet loglevel=3 oops=panic panic=-1"
