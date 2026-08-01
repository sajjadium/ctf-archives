#!/bin/sh

set -eu

cd "$(dirname "$0")"

curl -fsSL https://github.com/aqilc/chasm/raw/refs/heads/main/asm_x64.h -o asm_x64.h
curl -fsSL https://github.com/aqilc/chasm/raw/refs/heads/main/asm_x64.c -o asm_x64.c

echo "Dependencies downloaded. Run './build.sh' to build the program."
