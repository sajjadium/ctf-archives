#! /bin/sh
#
# run.sh
# Copyright (C) 2022 hal <hal@server20>
#
# Distributed under terms of the MIT license.
#


timeout --foreground 60 qemu-system-aarch64 \
    -m 128M \
    -machine virt \
    -cpu max \
    -kernel ./Image \
    -append "console=ttyAMA0 loglevel=3 oops=panic panic=1" \
    -initrd ./initramfs.cpio.gz \
    -monitor /dev/null \
    -smp cores=1,threads=1 \
    -nographic
