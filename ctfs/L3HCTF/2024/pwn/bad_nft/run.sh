#! /bin/sh

qemu-system-aarch64 \
    -m 256M \
    -machine virt \
    -cpu max \
    -kernel ./Image \
    -append "console=ttyAMA0 loglevel=3 quiet oops=panic panic=0" \
    -initrd ./rootfs.cpio \
    -smp 2 \
    -monitor /dev/null \
    -gdb tcp::54321 \
    -nographic
