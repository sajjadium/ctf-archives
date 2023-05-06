#!/bin/sh
# use PREBUILT_BINARIES/initramfs.cpio.gz as the -initrd argument if you want to use the pre-built one.
# if you want to build it yourself, leave it as-is.
qemu-system-x86_64 -nographic \
	-cpu qemu64,+pku,+xsave -m 512 \
	-nic user,id=net,ipv4=on,ipv6=off,restrict=on,hostfwd=tcp:127.0.0.1:1337-10.0.2.1:1234,model=virtio-net-pci \
	-object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-pci,rng=rng0 \
	-kernel PREBUILT_BINARIES/bzImage \
	-initrd runner/initramfs.cpio.gz \
	-append "console=ttyS0 ip=10.0.2.1::10.0.2.2:255.255.255.0"
