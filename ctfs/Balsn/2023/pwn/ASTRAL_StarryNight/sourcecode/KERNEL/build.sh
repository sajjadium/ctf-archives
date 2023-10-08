#!/bin/bash

gcc -masm=intel -nostdlib -fno-builtin entry.S panic.S syscall.S interruptEntry.S elf.c hypercall.c kernel.c memory.c syscall.c applet.c -o kernel
