# sample solve script to interface with the server
from pwn import *

# feel free to change this
account_metas = [
    ("program", "-r"), # readonly
    ("user", "sw"), # signer + writable
    ("vault", "-w"), # writable
    ("sailor union", "-w"),
    ("registration", "-w"),
    ("rich boi", "-r"),
    ("system program", "-r"),
]
instruction_data = b"placeholder"

p = remote("challs.actf.co", 31404)

with open("solve.so", "rb") as f:
    solve = f.read()

p.sendlineafter(b"program len: \n", str(len(solve)).encode())
p.send(solve)

accounts = {}
for l in p.recvuntil(b"num accounts: \n", drop=True).strip().split(b"\n"):
    [name, pubkey] = l.decode().split(": ")
    accounts[name] = pubkey

p.sendline(str(len(account_metas)).encode())
for (name, perms) in account_metas:
    p.sendline(f"{perms} {accounts[name]}".encode())
p.sendlineafter(b"ix len: \n", str(len(instruction_data)).encode())
p.send(instruction_data)

p.interactive()
