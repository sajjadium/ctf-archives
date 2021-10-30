#!/bin/bash

echo "Please provide your bot as executable file (script or ELF)"
read -p "Enter file size:" size

if [[ ! "$size" =~ ^[0-9]+$ ]] ; then
    echo "Not a Number"
    exit
fi

if [ "$size" -gt 10485760 ]; then
    echo "Too large!"
    exit
fi

echo "Now send the file"

stty_orig=`stty -g`
stty -echo
file="$(mktemp)"
cleanup() {
    rm -f "$file"
}
trap cleanup EXIT HUP INT TERM
dd of="$file" bs=1 count="$size" # status=none
stty $stty_orig

bios=""

EFI_ROM_DIR="$(dirname $(find /usr -name efi-e1000.rom 2>/dev/null))"
BIOS_ROM_DIR="$(dirname $(find /usr/share -name bios-256k.bin 2>/dev/null))"

[ ! -z "$EFI_ROM_DIR" ] && bios="$bios -L $EFI_ROM_DIR"
[ ! -z "$BIOS_ROM_DIR" ] && bios="$bios -L $BIOS_ROM_DIR"

if [ -z "$bios" ]; then
    echo "pleas install quemu-system and seabios"
    exit
fi

./qemu-system-x86_64 \
    -nographic \
    -nodefaults \
    -net none \
    -monitor none \
    -serial stdio \
    -m 128 \
    $bios \
    -device cloudinspect,id=cloudinspect \
    -drive format=raw,file="$file",snapshot=on,index=2 \
    -kernel vmlinuz-5.11.0-38-generic \
    -initrd initramfs.cpio.gz \
    -append console=ttyS0
