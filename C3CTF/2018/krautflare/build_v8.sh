#!/bin/bash

set -Eeuxo pipefail

fetch v8
pushd v8
git checkout dde25872f58951bb0148cf43d6a504ab2f280485
git apply < ../d8-strip-globals.patch
git apply < ../revert-bugfix-880207.patch
git apply < ../open_files_readonly.patch
gclient sync
./tools/dev/gm.py x64.release
popd
