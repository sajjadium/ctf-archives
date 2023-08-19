#!/bin/bash
echo "Your code please."

FOLDER=$(mktemp -d)
cp flag.txt "$FOLDER"
cd "$FOLDER"
mkdir src
cat <<EOF > Cargo.toml
[package]
name = "funsafe"
version = "0.1.0"
edition = "2021"
[lib]
name = "funsafe"
path = "src/lib.rs"
[[bin]]
name = "funsafe-bin"
path = "src/main.rs"
[dependencies]
ctor = "0.2"
[profile.release]
panic = "abort"
EOF

read program
echo "#![no_std] ${program//!/}" > src/lib.rs
echo "use funsafe::fun; pub fn main() {fun()}" > src/main.rs

RUSTFLAGS="$RUSTFLAGS -Funsafe-code -Zsanitizer=address" timeout 20 cargo +nightly run --target x86_64-unknown-linux-gnu --release

rm -rf "$FOLDER"