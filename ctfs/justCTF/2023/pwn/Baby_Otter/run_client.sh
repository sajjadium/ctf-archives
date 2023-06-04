set -eux

cd framework-solve/solve && sui move build
cd ..
cargo r --release
