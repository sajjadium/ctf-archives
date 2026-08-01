#!/bin/sh

set -eu

cd "$(dirname "$0")"

: "${CC:=gcc}"

"$CC" -o moosecalc moosecalc.c asm_x64.c -Wall -Wextra -lm
patchelf --set-interpreter ./ld-linux-x86-64.so.2 ./moosecalc
patchelf --set-rpath '$ORIGIN' ./moosecalc

chmod 755 ./moosecalc ./ld-linux-x86-64.so.2

echo "Build complete. Run './moosecalc' to execute the program."
