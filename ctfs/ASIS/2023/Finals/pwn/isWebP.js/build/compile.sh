#!/bin/sh
rm build -r 2>/dev/null
mkdir build
mkdir build/libwebp/
git clone https://chromium.googlesource.com/webm/libwebp/
cd libwebp
git checkout 7ba44f80f3b94fc0138db159afea770ef06532a0
git apply ../libwebp.patch
make -f ./makefile.unix -j4
find -name '*.a' | xargs -I '{}' cp '{}' ../build/libwebp
cd ..
git clone https://github.com/bellard/quickjs.git
cd quickjs
git checkout 2ee6be705fde0eb68acec25915d2947de1207abb
git apply ../quickjs.patch
cd ..
cp ./quickjs/* ./build -r
cd build
make qjs -j4
realpath ./qjs
