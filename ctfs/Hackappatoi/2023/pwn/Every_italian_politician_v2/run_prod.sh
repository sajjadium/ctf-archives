#!/bin/bash
while true
do
    qemu-system-xtensa -cpu esp32 -M esp32 -m 4M -drive file=flash.bin,if=mtd,format=raw -nic user,model=open_eth,hostfwd=tcp::80-:80 &
    qemu_pid=$!
    sleep 20
    kill -9 $qemu_pid
done
