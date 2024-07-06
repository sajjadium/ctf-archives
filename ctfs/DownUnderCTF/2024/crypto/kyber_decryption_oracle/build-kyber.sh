#!/bin/sh

git clone https://github.com/pq-crystals/kyber.git
cd kyber/ref
git checkout 441c0519a07e8b86c8d079954a6b10bd31d29efc
gcc -shared -fPIC -DKYBER_K=2 randombytes.c fips202.c aes256ctr.c sha256.c sha512.c symmetric-aes.c symmetric-shake.c indcpa.c polyvec.c poly.c ntt.c cbd.c reduce.c verify.c kem.c -o libpqcrystals_kyber512_ref.so
cp libpqcrystals_kyber512_ref.so ../../libpqcrystals_kyber512_ref.so
cd ../../
rm -rf kyber
