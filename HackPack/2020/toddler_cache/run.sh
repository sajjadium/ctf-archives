#!/bin/bash

VERSION="./glibc_versions"
VER="2.26"
TARGET="./toddler_cache"

curr_interp=$(readelf -l "$TARGET" | grep 'Requesting' | cut -d':' -f2 | tr -d ' ]')
target_interp="$VERSION/ld-$VER.so"

if [[ $curr_interp != $target_interp ]];
then
    patchelf --set-interpreter "$target_interp" "$TARGET"
fi

LD_PRELOAD="$VERSION/libc-$VER.so" "$TARGET"
