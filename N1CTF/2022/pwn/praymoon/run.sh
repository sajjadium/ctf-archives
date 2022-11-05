#!/bin/sh
qemu-system-x86_64 \
    -m 128M \
    -kernel ./bzImage \
    -initrd ./rootfs.cpio \
    -monitor /dev/null \
    -append "root=/dev/ram console=ttyS0 oops=panic panic=1 quiet kaslr" \
    -cpu kvm64,+smep,+smap\
    -netdev user,id=t0, -device e1000,netdev=t0,id=nic0 \
    -nographic \
    -no-reboot
