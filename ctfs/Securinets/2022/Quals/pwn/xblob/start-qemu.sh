#!/bin/sh
timeout --foreground 300 qemu-system-x86_64 \
        -m 64M \
        -nographic \
        -kernel bzImage \
        -append "rootwait root=/dev/vda console=ttyS0 loglevel=3 oops=panic panic=-1 pti=on kaslr" \
        -no-reboot \
        -cpu kvm64,+smap,+smep \
        -smp 2 \
        -monitor /dev/null \
        -drive file=rootfs.ext2,if=virtio,format=raw \
        -net nic,model=virtio \
        -net user
