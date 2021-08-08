#!/bin/sh
qemu-system-x86_64 -s\
    -m 512M \
    -cpu kvm64,+smep \
    -kernel vmlinuz \
    -initrd initramfs.cpio.gz \
    -snapshot \
    -nographic \
    -monitor /dev/null \
    -no-reboot \
    -append "console=ttyS0 nokaslr kpti=1 quiet panic=1"
