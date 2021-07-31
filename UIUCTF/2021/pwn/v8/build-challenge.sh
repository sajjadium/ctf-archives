#!/bin/bash

#
# Builds the UIUCTF 2021 "should've had a V8" challenge.
#

set -e
set -x

# Run everything from the same directory as the script so we can use relative paths.
cd "$(dirname "$0")"

# Checkout Depot Tools if it hasn't been checked out already.
if [ ! -d depot_tools ]; then
    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
fi

# Add Depot Tools to our path.
export PATH=$PATH:`pwd`/depot_tools

# Clone v8 repo if it hasn't already been.
if [ ! -d v8 ]; then
    mkdir -p v8
    cd v8
    fetch v8

    # Checkout a specific version.
    cd v8
    git fetch --tags
    git checkout -b 9.1.269.36 tags/9.1.269.36
    gclient sync -D --with_branch_heads
    cd ../..
fi

# Apply the patch.
cd v8/v8
patch -s -p1 < ../../diff.patch
cd ../..

# Build the code.
cd v8/v8
gn gen out/x64.release --export-compile-commands --args="is_debug=false"
ninja -C out/x64.release v8_hello_world
