#!/bin/sh
CPU=${CPU:-2}
MEM=${MEM:-512M}
exec qemu-system-x86_64 \
    -smp $CPU -m $MEM \
    -kernel vmlinuz \
    -initrd initramfs.cpio.gz \
    -hdb flag.txt \
    -snapshot \
    -nographic \
    -monitor /dev/null \
    -no-reboot \
    -append "console=ttyS0" \
    -device virtio-rng-pci \
    -net nic,model=e1000 \
    -net user,hostfwd=tcp::11111-:1024
