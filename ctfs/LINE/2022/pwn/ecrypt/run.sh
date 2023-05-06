#!/bin/sh
timeout --foreground -s SIGKILL 300 qemu-system-x86_64 -cpu kvm64,+smep,+smap \
  -m 64M \
  -kernel ./bzImage \
  -drive file=./rootfs.ext4,format=raw -snapshot \
  -nographic \
  -monitor /dev/null \
  -no-reboot \
  -append "root=/dev/sda rw console=ttyS0 loglevel=3 oops=panic panic=1 kaslr" 2>/dev/null
