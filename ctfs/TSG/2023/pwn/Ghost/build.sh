#!/bin/sh

cargo build --release
cp target/release/ghost ../dist/
