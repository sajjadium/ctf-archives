#!/bin/sh

# There are two subtle config changes happening which make the standalone build differ slightly from the pre-built shared binaries
# Differences:
# - libsasl.so is added as dependency
# - libchrome_zlib.so added as dependency
# - libc++.so added as dependency
#
# You can still use this build for prototyping, printfs, etc.
# However, the real exploit should work with the pre-built binaries.

DIR=/angle/out/Release
INC=/angle/include

cp $DIR/libc++.so libs/.
cp $DIR/libabsl.so libs/.
cp $DIR/libchrome_zlib.so libs/.
cp $DIR/libEGL.so libs/.
cp $DIR/libGLESv2.so libs/.
cp $DIR/libvulkan.so.1 libs/.
cp $DIR/libvk_swiftshader.so libs/.
cp $DIR/libfeature_support.so libs/.
cp $DIR/vk_swiftshader_icd.json libs/.
cp $DIR/libVkLayer_khronos_validation.so libs/.
cp -r $DIR/angledata libs/.

g++ main.cpp -DFPNG_NO_SSE=1 -I/fpng/src/ -Wall -Werror -O2 -g -I$INC -L./libs -lEGL -lGLESv2 -lchrome_zlib -labsl -lc++ -std=c++14 -o hxp_gpu
