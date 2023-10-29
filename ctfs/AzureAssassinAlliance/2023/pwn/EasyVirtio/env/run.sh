#!/bin/bash
timeout --foreground 300 ./qemu-system-x86_64 \
    -L pc-bios \
    -m 1024 \
    -kernel bzImage \
    -initrd rootfs.cpio \
    -object cryptodev-backend-builtin,id=cryptodev0 \
    -device virtio-crypto-pci,id=crypto0,cryptodev=cryptodev0 \
    -append "priority=low console=ttyS0" \
    -monitor /dev/null \
    -nographic
