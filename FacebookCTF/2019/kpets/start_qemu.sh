#!/bin/sh

# Start the QEMU image with a timeout
# $1 should be /path/to/bzImage
# $2 should be /path/to/initramfs.cpio
[ $# -lt 2 ] && { echo Usage: $0 /path/to/bzImage /path/to/initramfs.cpio; exit; }

timeout --foreground 120 \
qemu-system-x86_64 \
    -m 64M -smp 1,cores=1,threads=1 \
    -cpu host \
    --enable-kvm \
    -kernel $1 \
    -nographic \
    -append "console=ttyS0 noapic quiet" \
    -initrd $2 \
    -monitor /dev/null \
    2>/dev/null

