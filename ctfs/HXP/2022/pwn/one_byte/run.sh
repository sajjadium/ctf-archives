#!/bin/sh
# ./run.sh [qemu-args...]
# To copy a binary to /bin/pwn, specify something like
#   -drive id=pwn,file=[path],format=raw,if=virtio
# To enable the monitor, pass
#   -serial mon:stdio
# For debugging, pass
#   -s

qemu-system-x86_64 \
    -drive id=flag,file=flag.txt,format=raw,if=virtio \
    -cpu qemu64,+smap,enforce \
    -m 256 \
    -kernel vmlinuz \
    -initrd initramfs.cpio.gz \
    -append 'console=ttyS0 oops=panic panic=1 pti=on quiet' \
    -monitor none \
    -no-reboot \
    -snapshot \
    -nographic \
    "$@"
