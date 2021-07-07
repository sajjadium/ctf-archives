#!/bin/sh

cd $(dirname $0)

exec timeout -s KILL 60m ./qemu-system-x86_64 \
    -L ./pc-bios \
    -m 128M \
    -cpu qemu64,+smep,+smap \
    -smp 2 \
    -kernel ./vmlinuz \
    -initrd ./initramfs.cpio \
    -append "console=ttyS0 root=/dev/ram rw rdinit=/sbin/init kaslr pti=on oops=panic panic=1 quiet" \
    -device ss \
    -monitor none \
    -nographic

