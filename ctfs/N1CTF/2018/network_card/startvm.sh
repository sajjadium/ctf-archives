#!/bin/bash

qemu-system-x86_64 \
    -m 64M \
    -nographic \
    -kernel bzImage \
    -append 'console=ttyS0 loglevel=3 oops=panic panic=1 kaslr' \
    -monitor /dev/null \
    -initrd initramfs.img \
    -smp cores=1,threads=1 \
    -cpu qemu64,+smep,+smap \
    # -fsdev local,id=root,path=/tmp,security_model=none -device virtio-9p-pci,fsdev=root,mount_tag=shared \
    # -s \