#!/bin/bash

qemu-system-x86_64 \
  -m 128M \
  -nographic \
  -kernel ./bzImage \
  -append 'pti=on console=ttyS0 loglevel=1 oops=panic panic=1 kaslr' \
  -monitor /dev/null \
  -initrd ./rootfs.cpio \
  -cpu qemu64,+smep,+smap \
  -smp cores=2
