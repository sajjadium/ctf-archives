#!/bin/bash
wget https://download.qemu.org/qemu-5.2.0.tar.xz
tar xf qemu-5.2.0.tar.xz
cd qemu-5.2.0
patch -p1 < ../patch
mkdir build
cd build
../configure --target-list=riscv64-linux-user
make -j$(nproc)
