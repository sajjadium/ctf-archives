#!/bin/bash

git clone https://github.com/pq-crystals/dilithium.git
cd dilithium/ref
git checkout 3e9b9f1412f6c7435dbeb4e10692ea58f181ee51
git apply ../../my.patch
gcc -shared -fPIC -DDILITHIUM_RANDOMIZED_SIGNING=1 -DDILITHIUM_MODE=2 sign.c packing.c polyvec.c poly.c ntt.c reduce.c rounding.c symmetric-shake.c fips202.c randombytes.c -o libpqcrystals_dilithium2_ref.so 
mv libpqcrystals_dilithium2_ref.so ../../libpqcrystals_dilithium2_ref.so
cd ../../
rm -rf dilithium
