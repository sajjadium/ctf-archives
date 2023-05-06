#!/bin/bash
wget https://www.php.net/distributions/php-7.4.7.tar.bz2
tar xf php-7.4.7.tar.bz2
cd php-7.4.7
mkdir bld
cd bld
../configure --disable-all
make -j8
make install
