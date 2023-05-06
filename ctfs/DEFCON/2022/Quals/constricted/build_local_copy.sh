#!/bin/bash

mkdir boa -p
cd boa
if [ ! -d ".git" ]; then
    git init
    git remote add origin https://github.com/boa-dev/boa
    git fetch --depth 1 origin a357a18fcc91f720679d163a1531175f0001ebb0 
    git checkout FETCH_HEAD
    git apply ../constricted.patch
fi
cargo build -p boa_cli
./target/debug/boa
