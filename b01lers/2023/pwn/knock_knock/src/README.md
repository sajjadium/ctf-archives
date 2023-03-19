# Build

install required tools for building

	sudo pacman -S nasm lld grub
	cargo install cargo-sysroot

on debian, you may also have to install

	sudo apt install grub-pc

set toolchain and build sysroot

	rustup override set nightly
	./build.sh sysroot

if building sysroot fails, you may have to install rust-src

	rustup component add rust-src

compile with script

	./build.sh
