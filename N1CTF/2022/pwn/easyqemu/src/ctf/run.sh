#!/bin/sh
/qemu-system-x86_64 \
    -kernel /vmlinuz-5.0.5-generic \
    -append "root=/dev/ram rw console=ttyS0 oops=panic panic=1 nokaslr quiet" \
    -cpu kvm64 \
    -m 128M \
    -initrd /rootfs.cpio \
    -L pc-bios \
    -monitor /dev/null \
    -nographic \
    -no-reboot \
    -device uusb \
