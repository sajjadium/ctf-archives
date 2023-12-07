#!/bin/bash
setsid qemu-system-xtensa -cpu esp32 -M esp32 -m 4M -drive file=flash.bin,if=mtd,format=raw -nic user,model=open_eth,hostfwd=tcp::80-:80 -s &
qemu_pid=$!
sleep 5
/root/.espressif/tools/xtensa-esp-elf-gdb/12.1_20221002/xtensa-esp-elf-gdb/bin/xtensa-esp32-elf-gdb /root/every-italian-politician.elf -ex "target remote:1234"
kill -9 $qemu_pid
