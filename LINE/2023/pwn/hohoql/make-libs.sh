#!/bin/bash

CC=${CC:-clang-15}
CXX=${CXX:-clang++-15}
CFLAGS=''

if [ ! -d "tree-sitter" ]; then git clone https://github.com/tree-sitter/tree-sitter -b v0.20.7; fi
if [ ! -d "tree-sitter-cpp" ]; then git clone https://github.com/tree-sitter/tree-sitter-cpp -b v0.20.0; fi

mkdir -p build
rm -f build/*.o

$CXX -O1 -Itree-sitter-cpp/src -c tree-sitter-cpp/src/scanner.cc -o build/scanner.o
$CC  -O0 -Itree-sitter-cpp/src -c tree-sitter-cpp/src/parser.c -o build/parser.o

cd tree-sitter
CC=$CC CXX=$CXX make
cp *.so* ../build
cd ..


