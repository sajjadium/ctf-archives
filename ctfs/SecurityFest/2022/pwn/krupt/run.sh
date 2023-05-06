#!/bin/sh
qemu-system-x86_64 \
    -m 128M \
    -kernel ./bzImage \
    -initrd ./root.fs.gz  \
    -append 'console=ttyS0 rdinit=/sbin/init loglevel=3 oops=panic panic=1' \
    -no-reboot \
    -nographic \
    -monitor /dev/null 2>/dev/null
