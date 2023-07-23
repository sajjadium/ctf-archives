#!/bin/bash 

mkdir initramfs
(cd initramfs && cpio -idv < ../initramfs.cpio)
