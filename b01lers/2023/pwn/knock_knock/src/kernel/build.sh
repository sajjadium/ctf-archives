#!/bin/bash

OUT_BIN=kernel.bin

cd $(dirname $0)
[[ $1 = clean ]] && { cargo clean; exit 0; }
[[ $1 = sysroot ]] && { cargo sysroot; exit 0; }
[[ $1 = fmt ]] && { cargo fmt; exit 0; }
[[ $1 = release ]] && RFLAG=--release

if [[ $1 = test ]]
then
  IMG=$(cargo test --no-run --message-format=json 2> /dev/null | jq 'select(.executable) | .executable' | cut -d '"' -f 2)
else
  cargo build $RFLAG || exit 1

  IMG=target/x86_64-os-kernel/debug/kernel
  [[ $1 = release ]] && IMG=target/x86_64-os-kernel/release/kernel
fi

echo $IMG
if [[ $IMG -nt $OUT_BIN ]]
then
  cp $IMG $OUT_BIN
fi


exit 0
