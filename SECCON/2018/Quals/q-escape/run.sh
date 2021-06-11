#!/bin/sh
./qemu-system-x86_64 \
	-m 64 \
	-initrd ./initramfs.igz \
	-kernel ./vmlinuz-4.15.0-36-generic \
	-append "priority=low console=ttyS0" \
	-nographic \
	-L ./pc-bios \
	-vga std \
	-device cydf-vga \
	-monitor telnet:127.0.0.1:2222,server,nowait
