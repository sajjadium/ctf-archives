#!/bin/sh

# The monitor is necessary to send mouse and keyboard events to write the address.
# For debugging, you may want to replace -nographic with -s

qemu-system-x86_64 \
	-cpu qemu64 \
	-smp 1 \
	-m 128 \
	-serial mon:stdio \
	-snapshot \
	-no-reboot \
	-boot a \
	-fda kolibri.img \
	-hda flag.img \
	-nographic

