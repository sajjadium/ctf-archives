#! /bin/sh

qemu-system-riscv64 \
    -machine virt \
    -bios none \
    -kernel kernel \
    -m 128M \
    -smp 1 \
    -nographic \
    -drive file=fs.img,if=none,format=raw,id=x0 \
    -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 \
    -monitor null
