#!/bin/sh
timeout --foreground 300 qemu-system-x86_64 \
        -m 64M \
        -nographic \
        -kernel bzImage \
        -append "console=ttyS0 loglevel=3 oops=panic panic=-1 pti=on nokaslr" \
        -no-reboot \
        -cpu kvm64,+smap,+smep \
        -smp 1 \
        -monitor /dev/null \
        -initrd rootfs.cpio \
        -net nic,model=virtio \
        -net user
