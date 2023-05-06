#!/bin/sh

./qemu-system-x86_64 \
    -kernel bzImage \
    -initrd init.cpio \
    -monitor /dev/null \
    -nographic \
    -smp 1 \
    -cpu qemu64,+smep,+smap,+rdrand \
    -m 256 \
    -no-reboot \
    -L ./bios \
    -append "console=ttyS0 quiet loglevel=0 pti=on kaslr"
