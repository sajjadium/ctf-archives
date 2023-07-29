#!/bin/sh

./qemu-system-x86_64 \
    -m 4096M \
    -smp 1 \
    -kernel "./bzImage" \
    -append "console=ttyS0 panic=-1 ignore_loglevel pti=on" \
    -netdev user,id=net \
    -device e1000,netdev=net \
    -display none \
    -vga none \
    -serial stdio \
    -monitor /dev/null \
    -machine q35,smm=on,accel=tcg \
    -cpu max \
    -initrd "./initramfs.cpio.gz" \
    -global driver=cfi.pflash01,property=secure,value=on \
    -drive if=pflash,format=raw,unit=0,file=./FV/OVMF_CODE.fd,readonly=on \
    -drive if=pflash,format=raw,unit=1,file=./FV/OVMF_VARS.fd,readonly=on \
    -global ICH9-LPC.disable_s3=1 \
    -debugcon file:/dev/null \
    -global isa-debugcon.iobase=0x402 \
    -no-reboot 
    
