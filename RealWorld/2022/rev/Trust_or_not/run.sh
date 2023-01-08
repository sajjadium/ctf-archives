#!/bin/sh

qemu-system-aarch64 \
	-nographic \
	-smp 2 \
	-machine virt,secure=on,gic-version=3,virtualization=false \
	-cpu cortex-a57 \
	-d unimp -semihosting-config enable=on,target=native \
	-m 1024 \
	-bios bl1.bin \
	-initrd rootfs.cpio.gz \
	-kernel Image -no-acpi \
	-append console="ttyAMA0,38400 keep_bootcon root=/dev/vda2  -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-pci,rng=rng0,max-bytes=1024,period=1000" \
	-no-reboot \
	-monitor null

