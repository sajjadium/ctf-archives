#!/bin/bash

cd /home/ctf
tmp=`date +%N`
cp rootfs.img $tmp
qemu-system-x86_64 -hda $tmp -kernel 5.0.0-bzImage -append 'console=ttyS0 root=/dev/sda rw quiet' -m 128M --nographic -cpu kvm64,+smep,+smap
rm $tmp
exit 0
