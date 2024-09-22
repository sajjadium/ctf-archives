#!/bin/bash

cd rootfs-debug
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../iso/boot/initramfs.cpio.gz
cd ..

rm debug.iso
grub-mkrescue -o debug.iso ./iso/

rm debug.vhd
qemu-img resize -f raw debug.iso $(./calc.sh debug.iso debug.vhd)
qemu-img convert -f raw -o subformat=fixed,force_size -O vpc debug.iso debug.vhd
