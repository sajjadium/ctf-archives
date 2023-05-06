#!/bin/bash

cd chall && cargo build-bpf
cd ..
cargo build --release