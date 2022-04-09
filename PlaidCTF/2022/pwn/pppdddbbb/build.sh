#!/bin/sh
set -e

clang++ \
  -std=c++2a \
  -stdlib=libc++ \
  -O2 \
  -g \
  -fPIE \
  -pie \
  -Wl,-z,relro,-z,now \
  -Wa,--noexecstack \
  -D_FORTIFY_SOURCE=2 \
  -fstack-protector-strong \
  -fno-exceptions \
  problem.cc \
  -lpthread \
  -o problem
