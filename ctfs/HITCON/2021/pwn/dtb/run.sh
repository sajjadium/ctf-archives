#!/bin/bash

qemu-system-aarch64 -M virt,dtb=example.dtb \
  -nographic -monitor none \
  -smp 1 -m 2048 \
  -kernel ./Image.gz -append "console=ttyAMA0 panic=-1 oops=panic" \
  -initrd ./rootfs.cpio.gz \
  -no-reboot -cpu cortex-a72
