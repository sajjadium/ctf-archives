#!/bin/bash

wget 'https://www.zsh.org/pub/zsh-5.9.tar.xz'
tar xf ./zsh-5.9.tar.xz
cp ./note.c ./note.mdd ./zsh-5.9/Src/Modules/ 
cd zsh-5.9
./Util/preconfig
EXELDFLAGS= LIBLDFLAGS= CFLAGS="-g -O0" ./configure
make

