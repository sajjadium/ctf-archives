#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

timeout --foreground 300 /usr/bin/qemu-system-x86_64 \
	-m 128M \
	-cpu kvm64,+smep,-smap \
	-smp 2 \
	-kernel $SCRIPT_DIR/bzImage \
	-initrd $SCRIPT_DIR/initramfs.cpio.gz \
	-nographic \
	-monitor none \
	-append "console=ttyS0 kaslr quiet panic=1" \
	-no-reboot
