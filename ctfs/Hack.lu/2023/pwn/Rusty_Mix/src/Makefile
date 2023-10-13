
clean:
	rm -f rustymix
	cargo clean

rustymix:
	cargo build
	gcc -g -Wl,-z,relro,-z,now -o rustymix c_src/main.c ./target/debug/librustymix.a

all: rustymix
