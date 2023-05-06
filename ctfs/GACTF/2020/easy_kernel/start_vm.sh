#!/bin/sh

qemu-system-x86_64 \
     -initrd rootfs.img \
     -kernel bzImage \
     -append 'console=ttyS0 root=/dev/sda rw quiet panic=1 kaslr' \
     -m 128M \
     --nographic \
     -monitor /dev/null \
     -cpu kvm64,+smep,+smap
     