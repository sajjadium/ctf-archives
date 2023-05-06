#!/bin/bash

./qemu-system-x86_64 \
  -L ./pc-bios \
  -kernel ./bzImage \
  -initrd ./rootfs.cpio.gz \
  -nographic \
  -cpu qemu64,+smep,+smap \
  -net nic,model=virtio -net user \
  -monitor /dev/null \
  -append "console=ttyS0 loglevel=0 kaslr" -no-reboot
