#!/bin/sh

timeout --foreground 300s qemu-system-x86_64 \
	-m 128M \
	-nographic \
	-kernel "./bzImage" \
	-append "console=ttyS0 pti=on" \
	-monitor /dev/null \
	-initrd "./initramfs.cpio.gz" \
	-enable-kvm \
	-cpu Skylake-Client \
	-no-reboot