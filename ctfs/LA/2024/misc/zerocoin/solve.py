#!/usr/bin/env python3

from pwn import *

p = remote("chall.lac.tf", 31337)

addrs = {}
while True:
    name = p.recvuntil(b": ", drop=True).decode()
    if name == "program pubkey":
        break
    key = p.recvline(keepends=False).decode()
    addrs[name] = key

print(addrs)

# can change pubkey to anything else, this is just a randomly generated valid pubkey
p.sendline(b"2vXNNmancsQhSnuMBPQo2AfNdxRKijNe9pb44sGBbkY8")

# copy solve.so to cwd or change this path to ./solve/sbf-solana-solana/release/solve.so
with open("solve.so", "rb") as f:
    solve = f.read()

p.sendlineafter(b"program len: \n", str(len(solve)).encode())
p.send(solve)

# can change accounts, s means signer, r/w means readonly/writable
accounts = """
user: sw
vault: -w
mint: -w
user_token: -w
program: -r
token_program: -r
system_program: -r
"""

accounts = [l.split(": ") for l in accounts.strip().split("\n")]
p.sendlineafter(b"num accounts: \n", str(len(accounts)).encode())
p.sendline("\n".join(f"{b} {addrs[a]}" for (a, b) in accounts).encode())

# can add data to the instruction
ix_data = b"filler data"

p.sendlineafter(b"ix len: \n", str(len(ix_data)).encode())
p.send(ix_data)

p.interactive()
