#!/bin/bash

cd `dirname $0`
qemu-system-x86_64 \
	-initrd rootfs.cpio \
	-kernel  bzImage\
	-append 'console=ttyS0 root=/dev/ram oops=panic panic=1 quiet kaslr'  \
	-monitor /dev/null \
	-m 64M \
   	--nographic \
	-smp cores=2,threads=2 \
	-cpu kvm64,+smep,smap  \
	#-s
