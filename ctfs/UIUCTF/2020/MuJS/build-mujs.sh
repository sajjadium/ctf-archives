#!/usr/bin/env bash

set -e
set -x

[ ! -d "mujs" ] && unzip mujs.zip

mkdir -p mujs-build
cd mujs-build
cmake ../mujs
make
