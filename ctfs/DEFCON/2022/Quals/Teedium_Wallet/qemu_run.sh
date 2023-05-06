#!/bin/bash

# semihosting needed for bootloaders - bl2.bin, bl32.bin, bl32_extra1.bin, bl33.bin - QEMU is built to disable semihosting after boot

./qemu-system-arm \
    -nographic \
    -serial chardev:serial0 \
    -serial /dev/null \
    -monitor /dev/null \
    -chardev stdio,signal=off,id=serial0 \
    -smp 2 \
    -machine virt,secure=on \
    -cpu cortex-a15 \
    -semihosting-config enable=on,target=native \
    -m 1057 \
    -bios bl1.bin \
    -object rng-random,filename=/dev/urandom,id=rng0 \
    -device virtio-rng-pci,rng=rng0,max-bytes=1024,period=1000 \
    -netdev user,id=vmnic -device virtio-net-device,netdev=vmnic \
    -no-reboot \
