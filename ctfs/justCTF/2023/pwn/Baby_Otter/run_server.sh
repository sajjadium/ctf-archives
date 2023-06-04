set -eux

cd framework/chall && sui move build 
cd .. 
cargo r --release
