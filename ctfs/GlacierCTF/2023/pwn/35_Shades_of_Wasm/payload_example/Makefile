wasi-sdk=/opt/wasi-sdk

payload: payload.c
	$(wasi-sdk)/bin/clang payload.c --target=wasm32-unknown-wasi --sysroot $(wasi-sdk)/share/wasi-sysroot/ \
    -O0 -g -o payload.wasm
	base64 payload.wasm -w 0 > payload.wasm.base64

all: payload
