#!/bin/sh
# Boot a RISC-V VM with a software TPM listening on the network
set -eu

cd "$(dirname -- "$0")"

if ! command -v qemu-system-riscv64 > /dev/null 2>&1 ; then
    echo >&2 "qemu-system-riscv64 not found. If you are using Debian or Ubuntu:"
    echo >&2 "    sudo apt-get install qemu-system-misc"
    exit 1
fi

qemu-system-riscv64 \
    -nographic \
    -machine virt \
    -m 128M \
    -bios riscv64-linux-gnu_opensbi_fw_jump.elf \
    -kernel vmtpm-kernel \
    -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-device,rng=rng0 \
    -netdev user,id=net0,restrict=y,hostfwd=tcp:127.0.0.1:2321-:2321 \
    -device virtio-net-pci,netdev=net0
