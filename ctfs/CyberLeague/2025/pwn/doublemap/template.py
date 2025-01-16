#!/usr/bin/env python3

from pwn import *

elf = ELF("dist/bo")
if args.REMOTE:
    io = remote("localhost", 8080)
else:
    io = elf.process()

io.interactive()