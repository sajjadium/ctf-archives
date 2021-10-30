#!/bin/bash
if [ ! -d qemu ]; then
    git clone https://github.com/qemu/qemu
    git -C qemu checkout 'v5.2.0'
    git -C qemu apply "$(pwd)/diff_chall.txt"
else
    # save current changes, just in case
    git -C qemu add -N hw/misc/cloudinspect.c
    git -C qemu diff > "$(pwd)/diff_chall_save.txt"
    # delete if nothing new
    diff "$(pwd)/diff_chall_save.txt" "$(pwd)/diff_chall.txt" > /dev/null && rm "$(pwd)/diff_chall_save.txt"

    git -C qemu reset --hard origin/master
    git -C qemu pull
    git -C qemu checkout 'v5.2.0'
    git -C qemu apply "$(pwd)/diff_chall.txt"
fi
cd qemu

rm -rf build
mkdir build
cd build

../configure --target-list="x86_64-softmmu" \
    --audio-drv-list= \
    --disable-sdl \
    --disable-gtk \
    --disable-vte \
    --disable-brlapi \
    --disable-opengl \
    --disable-virglrenderer
make -j$(nproc)
