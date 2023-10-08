#!/bin/bash

gcc -masm=intel -nostdlib -fno-builtin entry.S user.c lib.c syscall.c -o user
