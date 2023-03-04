#!/bin/sh
OUT="$(mktemp /tmp/disk.redacted.bin.XXXXXXXXXX)"
cp ./disk.redacted.bin "$OUT"

timeout 5 qemu-system-x86_64 \
    -monitor /dev/null \
    -drive format=raw,file="$OUT" \
    -serial stdio \
    -m 512M \
    -display none \
    -no-reboot < sdk/main.bin

rm "$OUT"

