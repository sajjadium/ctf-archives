#!/bin/bash
set -e

git clone https://github.com/junkurihara/rust-rpxy

cd rust-rpxy
git switch --detach "0.6.1"

cat << EOF > .gitmodules
[submodule "submodules/h3"]
	path = submodules/h3
	url = https://github.com/junkurihara/h3.git
[submodule "submodules/quinn"]
	path = submodules/quinn
	url = https://github.com/junkurihara/quinn.git
[submodule "submodules/s2n-quic"]
	path = submodules/s2n-quic
	url = https://github.com/junkurihara/s2n-quic.git
[submodule "submodules/rusty-http-cache-semantics"]
	path = submodules/rusty-http-cache-semantics
	url = https://github.com/junkurihara/rusty-http-cache-semantics.git
EOF

git submodule update --init
git apply ../0001-logging-improvement.patch
