#!/bin/sh
set -e

make -C tests clean all
cargo test --release -p mooneye-gb-core --test mooneye_suite
