#!/bin/bash

./qemu-system-x86_64 \
    -cpu qemu64,-smap,-smep \
    -kernel bzImage \
    -initrd initramfs.cpio.gz \
    -append "console=ttyS0 quiet" \
    -nographic \
    -monitor /dev/null \
    -device driver=pza999,netdev=net0 \
    -netdev user,id=net0,hostfwd=udp::5555-:5556,ipv6=off
