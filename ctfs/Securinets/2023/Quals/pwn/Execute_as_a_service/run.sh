#!/bin/sh
#pushd fs
#find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../initramfs.cpio.gz
#popd

qemu-system-x86_64 \
	-m 512M\
	-kernel ./bzImage \
	-initrd ./initramfs.cpio.gz \
	-nographic \
	-no-reboot \
	-monitor none  \
   	-append "console=tty0 console=ttyS0,38400n7 kaslr kpti=1 debug panic=1" 

