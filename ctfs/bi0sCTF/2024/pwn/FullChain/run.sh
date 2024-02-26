#!/bin/sh
# $1 => JS file
# $2 => other exploits in archive to be placed at /tmp/file
./qemu-system-x86_64 \
    -L ./bin/ \
    -m 256M \
    -cpu kvm64,+smep,+smap \
    -kernel bzImage \
    -device virtio-note,disable-legacy=on \
    -drive file=rootfs.ext3,format=raw \
    -drive file=$1,format=raw \
    -drive file=$2,format=raw \
    -snapshot \
    -nographic \
    -monitor /dev/null \
    -no-reboot \
    -sandbox on,spawn=deny \
    -append "root=/dev/sda rw init=/init console=ttyS0 kaslr loglevel=3 oops=panic panic=-1"
