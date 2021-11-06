#!/bin/sh
timeout --foreground 300 qemu-system-x86_64 \
        -m 64M -smp 2 -nographic -no-reboot \
        -kernel bzImage \
        -initrd rootfs.cpio \
        -append "console=ttyS0 loglevel=3 oops=panic panic=-1 pti=on kaslr" \
        -cpu kvm64 -monitor /dev/null \
        -net nic,model=virtio -net user
