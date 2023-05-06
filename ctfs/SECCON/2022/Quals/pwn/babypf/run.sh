#!/bin/sh
qemu-system-x86_64 \
    -m 64M \
    -nographic \
    -kernel qemu/bzImage \
    -append "console=ttyS0 loglevel=3 oops=panic panic=-1 kaslr" \
    -no-reboot \
    -cpu kvm64,smap,smep \
    -monitor /dev/null \
    -initrd qemu/rootfs.cpio \
    -net nic,model=virtio \
    -net user
