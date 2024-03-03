#!/bin/bash

nasm -f ELF64 -o chall.o chall.asm
gcc -z noexecstack -o chall chall.o -nostdlib
rm chall.o
