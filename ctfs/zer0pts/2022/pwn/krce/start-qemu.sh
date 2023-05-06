#!/bin/sh
timeout --foreground 300 qemu-system-x86_64 \
     -m 64M \
     -nographic \
     -kernel bzImage \
     -append "console=ttyS0 loglevel=3 oops=panic panic=-1 pti=on kaslr" \
     -no-reboot \
     -cpu kvm64,+smap,+smep \
     -monitor /dev/null \
     -initrd rootfs.cpio
