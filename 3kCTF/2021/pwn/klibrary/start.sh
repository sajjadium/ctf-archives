#!/bin/sh

exec qemu-system-x86_64 \
    -m 128M \
    -nographic \
    -kernel "./bzImage" \
    -append "console=ttyS0 loglevel=3 oops=panic panic=-1 pti=on kaslr" \
    -no-reboot \
    -cpu qemu64,+smep,+smap \
    -monitor /dev/null \
    -initrd "./initramfs.cpio" \
    -smp 2 \
    -smp cores=2 \
    -smp threads=1 \
