#!/bin/sh
timeout --foreground 300 ./qemu-system-x86_64 \
    -device actf \
    -m 128M \
    -L ./pc-bios \
    -append "console=ttyS0" \
    -kernel bzImage \
    -initrd rootfs.cpio \
    -nographic \
    -no-reboot \
    -monitor /dev/null
