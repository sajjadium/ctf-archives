#!/bin/bash

cd solve && cargo build-bpf
cd ..
cargo build --release
