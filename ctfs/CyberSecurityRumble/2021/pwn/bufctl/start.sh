#!/bin/bash

timeout 5m qemu-system-x86_64 \
    -m 256M \
    -kernel 'bzImage' \
    -initrd 'rootfs.cpio.gz' \
    -append 'console=ttyS0 loglevel=3 oops=panic panic=1 kaslr' \
    -cpu qemu64,+smep,+smap \
    -no-reboot \
    -monitor /dev/null \
    -nographic
