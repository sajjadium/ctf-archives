#!/bin/bash
qemu-nbd --connect=/dev/nbd0 ./ZealOS.qcow2
mkdir -p /tmp/zealos
sleep 1
mount /dev/nbd0p1 /tmp/zealos/
cp Once.ZC /tmp/zealos/Home/
cp chall.ZC /tmp/zealos/Home/
cp HomeSys.ZC /tmp/zealos/Home/
cp flag.txt /tmp/zealos/Home/
umount /dev/nbd0p1
qemu-nbd --disconnect /dev/nbd0
