#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

timeout --foreground 180 /usr/bin/qemu-system-x86_64 \
	-m 64M \
	-cpu kvm64,+smep,+smap \
	-kernel $SCRIPT_DIR/bzImage \
	-initrd $SCRIPT_DIR/initramfs.cpio.gz \
	-nographic \
	-monitor none \
	-append "console=ttyS0 kaslr quiet panic=1" \
	-no-reboot
