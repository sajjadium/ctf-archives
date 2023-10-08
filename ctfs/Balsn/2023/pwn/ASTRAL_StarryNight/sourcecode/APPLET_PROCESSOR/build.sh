#!/bin/bash

wget https://raw.githubusercontent.com/jwang-a/CTF/master/utils/Pwn/SECCOMP.h
gcc -masm=intel -mno-red-zone processor.c jit.c device.c util.c sandbox.c -o processor -lssl -lcrypto
rm SECCOMP.h
