#!/bin/sh

# This file has been run in a clean Ubuntu 22.04 docker

set -e

apt update && apt install gcc make git libncurses-dev -y

# Latest tag while writing the challenge
git clone https://github.com/vim/vim.git --branch v9.0.1912 --single-branch --depth 1
cd vim
git apply < ../security.patch
git apply < ../jail.patch
git apply < ../bug.patch

./configure
make -j`nproc`

cp src/vim ../rust
