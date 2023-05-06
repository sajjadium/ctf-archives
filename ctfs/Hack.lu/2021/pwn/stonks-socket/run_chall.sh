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

qemu-system-x86_64 \
    -nographic \
    -nodefaults \
    -net none \
    -monitor none \
    -serial stdio \
    -m 128 \
    -drive format=raw,file=flag_disk,snapshot=on \
    -drive format=raw,file="$file",snapshot=on,index=2 \
    -kernel vmlinuz-5.11.0-38-generic \
    -initrd initramfs.cpio.gz \
    -append console=ttyS0
