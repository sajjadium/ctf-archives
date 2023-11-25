build: wasm_host/src/main.rs
	cd wasm_host && cargo build --release && cd ..
	cp wasm_host/target/release/wasm_host chall

debug: wasm_host/src/main.rs
	cd wasm_host && cargo build && cd ..

all: build
