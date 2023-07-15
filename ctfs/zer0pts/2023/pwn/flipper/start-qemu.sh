#!/bin/sh

timeout --foreground 300 qemu-system-x86_64 \
    -m 64M \
    -nographic \
    -kernel bzImage \
    -append "rootwait root=/dev/vda rw init=/init console=ttyS0 quiet oops=panic panic_on_warn=1 panic=-1" \
    -no-reboot \
    -cpu kvm64,+smap,+smep \
    -monitor /dev/null \
    -drive file=rootfs.ext2,if=virtio,format=raw \
    -snapshot
