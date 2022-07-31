#!/usr/bin/env sh

git clone https://github.com/WasmEdge/WasmEdge.git /root/WasmEdge

cd /root/WasmEdge
git checkout 0.10.0
mkdir -p build && cd build

cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DWASMEDGE_BUILD_AOT_RUNTIME=OFF \
    -DWASMEDGE_BUILD_TOOLS=OFF \
    -DWASMEDGE_BUILD_PLUGINS=OFF \
    ..
make -j

mkdir /root/export
cp -r /root/WasmEdge/build/include/api/wasmedge /root/export/
cp /root/WasmEdge/build/lib/api/libwasmedge_c.so /root/export/
