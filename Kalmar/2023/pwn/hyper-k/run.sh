#!/bin/sh

qemu-system-x86_64 \
    -enable-kvm -machine q35 -device intel-iommu \
    -kernel bzImage -initrd init.cpio \
    -m 256M \
    -nographic \
    -cpu host,+smep,+smap,+rdrand \
    -smp 8 \
    -monitor /dev/null \
    -append "console=ttyS0 quiet loglevel=0 kaslr pti=on" -no-reboot
