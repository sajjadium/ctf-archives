#!/bin/bash

set -Eeuxo pipefail

fetch v8
pushd v8
git checkout 8.1.307.31
git apply < ../0001-Remove-globals.patch
gclient sync
./tools/dev/gm.py x64.release
popd


