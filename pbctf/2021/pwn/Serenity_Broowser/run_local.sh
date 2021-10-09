#!/bin/sh

qemu-system-i386 -m 512M -cpu max -d guest_errors -no-reboot -smp 1 \
    -drive file=files/disk.qcow2,format=qcow2,index=0,media=disk -snapshot \
    -kernel files/Prekernel -initrd files/Kernel -enable-kvm