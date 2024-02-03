#!/bin/sh
qemu-system-x86_64 \
    -kernel bzImage \
    -cpu qemu64,+smep,+smap,+rdrand \
    -m 512M \
    -smp 2 \
    -initrd rootfs.cpio \
    -append "console=ttyS0 quiet loglevel=3 oops=panic panic_on_warn=1 panic=-1 pti=on page_alloc.shuffle=1 kaslr" \
    -monitor /dev/null \
    -nographic \
    -no-reboot
