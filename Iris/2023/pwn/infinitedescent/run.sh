#!/bin/sh
qemu-system-arm -machine lm3s6965evb -cpu cortex-m3 -m 4096 --chardev stdio,id=stdio -semihosting --semihosting-config enable=on,target=native,chardev=stdio -device loader,file=chal.elf -machine accel=tcg -d int,cpu_reset -display none 2>/dev/null
# to debug, add -s -S and connect with gdb-multiarch
