#!/bin/bash

rawdisk="$1"
vhddisk="$2"

MB=$((1024*1024))
size=$(qemu-img info -f raw --output json "$rawdisk" | gawk 'match($0, /"virtual-size": ([0-9]+),/, val) {print val[1]}' | tail -n 1)
rounded_size=$(((($size+$MB-1)/$MB)*$MB))

echo "$rounded_size"
