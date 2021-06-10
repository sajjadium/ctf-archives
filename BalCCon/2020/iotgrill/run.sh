#!/bin/sh
/usr/bin/qemu-system-arm -nographic -machine lm3s6965evb -cpu cortex-m3 \
    -kernel kernel.bin -monitor /dev/null -serial stdio
