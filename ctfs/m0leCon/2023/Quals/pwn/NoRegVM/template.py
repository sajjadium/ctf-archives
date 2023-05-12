#!/usr/bin/env python3

from pwn import *

r = remote("remote-addr", 3333)
# send files before interacting
code_file = open("challenge.vm", "rb")
r.send(code_file.read()+b'ENDOFTHEFILE')
code_file.close()
memory_file = open("strings.vm", "rb")
r.send(memory_file.read()+b'ENDOFTHEFILE')
memory_file.close()
r.recvuntil(b"Starting challenge...\n")

# Now you can interact with the challenge
r.interactive()
