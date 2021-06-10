#!/bin/sh
qemu-system-x86_64 \
    -nographic \
    -nodefaults \
    -net none \
    -monitor none \
    -serial stdio \
    -m 128M \
    -bios OVMF.fd \
    -drive format=raw,file=disk,snapshot=on \
    -drive format=raw,file=exploits,snapshot=on,index=2

