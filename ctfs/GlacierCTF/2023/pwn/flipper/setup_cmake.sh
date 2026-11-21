#!/usr/bin/env sh

# Use BUILD_DIR env var as path if provided, otherwise use default
DEFAULT_DIR="build"
BUILD_DIR="${BUILD_DIR:-${DEFAULT_DIR}}"

# Create the build directory and initialize cmake pointing to this source folder
cmake -B"${BUILD_DIR}" -H.

cd build
make -j
