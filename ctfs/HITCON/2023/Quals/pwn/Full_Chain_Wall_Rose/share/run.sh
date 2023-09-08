#!/bin/bash

qemu-system-x86_64 \
    -L /home/user/bios \
    -kernel /home/user/bzImage \
    -initrd /home/user/initramfs.cpio.gz \
    -cpu kvm64,+smep,+smap \
    -monitor none \
    -m 1024M \
    -append "console=ttyS0 oops=panic panic=1 quiet" \
    -monitor /dev/null \
    -nographic \
    -no-reboot \
    -net user -net nic -device e1000
