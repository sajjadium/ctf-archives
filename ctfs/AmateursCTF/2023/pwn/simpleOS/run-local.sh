#!/bin/sh

cp disk.img /tmp/disk.img

qemu-system-x86_64 \
    -drive format=raw,file=/tmp/disk.img,if=ide \
    -serial stdio \
    -nographic \
    -monitor telnet:127.0.0.1:1337,server,nowait \
    -m 20M