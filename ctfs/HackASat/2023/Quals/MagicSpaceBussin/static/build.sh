#!/bin/bash

cmake -DCMAKE_BUILD_TYPE=Release -B build .
cmake --build build

if [[ -n "$1" ]]; then
    cp build/magic $1
fi