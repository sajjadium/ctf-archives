#!/bin/sh

set -e
set -x 

CAPSTONE_DIR="capstone-5.0"
CAPSTONE_SRC=$CAPSTONE_DIR.tar.gz

rm -rf $CAPSTONE_DIR
export CC=arm-linux-gnueabi-gcc
export AR=arm-linux-gnueabi-ar
export RANLIB=arm-linux-gnueabi-ranlib

tar -xf $CAPSTONE_SRC
cd $CAPSTONE_DIR
./make.sh

cp libcapstone.so.5 ../libcapstone.so
cp libcapstone.a ../libcapstone.a
cp -r include ../
