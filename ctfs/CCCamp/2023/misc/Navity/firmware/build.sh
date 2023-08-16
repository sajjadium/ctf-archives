#!/usr/bin/env bash
mkdir -p build
cd build
arm-none-eabi-gcc -O0 -mcpu=cortex-m3 -mthumb ../firmware.c -specs=nano.specs -lc -lnosys -T../m3.ld -o firmware
arm-none-eabi-objcopy -O binary -S firmware firmware.bin