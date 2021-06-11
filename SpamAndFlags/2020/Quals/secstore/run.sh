#!/bin/bash

./qemu-system-aarch64 \
    -machine virt \
    -cpu max \
    -smp 2 \
    -kernel ./Image \
    -initrd ./initramfs.cpio.gz \
    -nic none \
    -nographic \
    -append "console=ttyAMA0" 
#    -append "console=ttyAMA0 nokaslr" \
#    -d trace:pl666*


# Qemu Notes

# This is not a qemu pwning challenge. 

# The included qemu binary was compiled on ubuntu 18.04
# If you want to compile and run it on your local system,
# use the commands below:

# git clone https://github.com/qemu/qemu.git qemu-git
# cd qemu-git/
# git checkout -b new_branch 17e1e49814096a3daaa8e5a73acd56a0f30bdc18
# patch -p1 < ../qemu.patch
# ./configure --target-list=aarch64-softmmu && make 
