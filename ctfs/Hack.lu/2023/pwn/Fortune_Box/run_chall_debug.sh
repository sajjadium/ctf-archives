#!/bin/sh

exec ./qemu-system-meta \
    -nographic \
    -net none \
    -display none \
    -monitor /dev/null \
    -device da,exit_threads=1 \
    -chardev stdio,id=chan0 \
    -chardev pty,id=chan1 \
    -chardev file,id=chan2,path=kmsg.log \
    -kernel kernel
