#!/bin/sh

exec ./qemu-system-meta \
    -nographic \
    -net none \
    -display none \
    -monitor /dev/null \
    -device da,exit_threads=1 \
    -chardev file,path=/dev/null,id=chan0 \
    -chardev stdio,id=chan1 \
    -kernel kernel
