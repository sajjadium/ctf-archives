#!/bin/sh
# use if you want to build everything and test locally
cd chess-wasm && wasm-pack build --no-typescript --release --target web && cd ..
cd app && cargo build --release && cd ..
cp chess-wasm/pkg/chess_wasm* app/static/js/
cd app && cargo run --release && cd ..