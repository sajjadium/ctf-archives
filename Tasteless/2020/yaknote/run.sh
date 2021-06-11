#!/bin/sh

qemu-system-x86_64 \
    -cpu qemu64,+smap,+smep \
    -m 256 \
    -nographic \
    -kernel bzImage \
    -initrd initrd.gz \
    -append "quiet console=ttyS0 nokaslr" \
    -nographic \
    -monitor /dev/null \
