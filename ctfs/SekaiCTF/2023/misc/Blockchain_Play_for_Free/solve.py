# sample solve script to interface with the server
import pwn

# feel free to change this
account_metas = [
    ("program", "-r"),  # read only
    ("data account", "-w"), # writable
    ("user", "sw"), # signer + writable
    ("user data", "sw"),
    ("system program", "-r"),
]
instruction_data = b"placeholder"

p = pwn.remote("0.0.0.0", 8080)

with open("solve.so", "rb") as f:
    solve = f.read()

p.sendlineafter(b"program pubkey: \n", b"placeholder")
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
