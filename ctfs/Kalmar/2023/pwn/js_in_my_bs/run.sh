#!/bin/sh
OUT="$(mktemp /tmp/output.XXXXXXXXXX)"
cp ./bootjs.bin "$OUT"

./qemu-system-i386 -L /bios -display none -drive format=raw,file="$OUT" -serial stdio

rm "$OUT"
