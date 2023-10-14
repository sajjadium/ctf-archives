#!/bin/sh

cd $(dirname $0)
exec timeout --foreground 600 ./qemu-system-x86_64 \
    -device note-service \
    -monitor /dev/null \
    -m 40M \
    -nographic \
    -kernel bzImage \
    -append "console=ttyS0 loglevel=1 oops=panic panic=-1 pti=on" \
    -no-reboot \
    -cpu kvm64,smap,smep \
    -initrd rootfs.cpio.gz \
    -net nic,model=virtio \
    -net user \
    -L /home/pwn/qemu/
