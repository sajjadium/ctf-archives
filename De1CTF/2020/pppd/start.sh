#!/bin/sh
/usr/bin/qemu-system-mipsel -kernel ./vmlinux -initrd ./rootfs.img -append 'root=/dev/ram console=ttyS0 rw physmap.enabled=0 noapic quiet log_level=0' -m 60M -nographic -monitor /dev/null -no-reboot -net none 2>/dev/null
