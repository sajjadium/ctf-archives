#!/bin/sh
qemu-system-x86_64 \
	-m 256M \
	-cpu kvm64,+smep,+smap \
	-smp cores=2,threads=2 \
	-kernel bzImage \
	-initrd ./rootfs.cpio \
	-nographic \
	-monitor /dev/null \
	-snapshot \
	-append "console=ttyS0 kaslr pti=on quiet oops=panic panic=1" \
	-no-reboot
