#!/bin/bash

#cp exploit initramfs
#cp packetdrv.ko initramfs/root
cd initramfs
find . | cpio -o -H newc -R root:root | gzip -9 > ../initramfs.cpio.gz
