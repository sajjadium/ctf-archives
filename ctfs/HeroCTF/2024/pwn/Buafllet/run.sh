#!/bin/sh

/usr/bin/qemu-system-aarch64 \
    -machine virt,mte=on \
    -cpu max \
    -M virt \
    -smp 2 \
    -initrd initramfs.cpio.gz \
    -kernel Image \
    -nographic \
    -append "kaslr pxn=1 pan=1 kpti=1 panic=1" \
    -virtfs local,path=/buafllet/exploit,mount_tag=host0,security_model=passthrough,id=host0