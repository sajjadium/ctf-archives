#!/bin/bash

cd rootfs-release
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../iso/boot/initramfs.cpio.gz
cd ..

rm release.iso
grub-mkrescue -o release.iso ./iso/

rm release.vhd
qemu-img resize -f raw release.iso $(./calc.sh release.iso release.vhd)
qemu-img convert -f raw -o subformat=fixed,force_size -O vpc release.iso release.vhd
