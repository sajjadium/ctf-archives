#!/bin/bash
rm -r ./build 2>/dev/null
mkdir build
cd build
wget https://www.lua.org/ftp/lua-5.4.6.tar.gz
tar xf lua-5.4.6.tar.gz
cd lua-5.4.6
git apply ../../lua.patch
make -j4
readlink -f src/lua
