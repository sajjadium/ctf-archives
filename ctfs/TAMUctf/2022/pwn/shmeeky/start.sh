#!/bin/bash

function cleanup {
  pkill -P $$
}
trap cleanup exit

qemu-system-x86_64 \
    -m 128M \
    -cpu kvm64 \
    -kernel bzImage \
    -initrd rootfs.cpio \
    -hdb flag.txt \
    -snapshot \
    -nographic \
    -monitor /dev/null \
    -no-reboot \
    -append "rootwait root=/dev/vda console=ttyS0 kpti=1 quiet panic=1 kaslr" \
