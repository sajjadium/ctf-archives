
from instancer.pow import solve_challenge
from pwn import *

# fill in port number here
p_gateway = remote("chall.pwnoh.io", ...)

# Solve the proof-of-work if enabled (limits abuse)
pow = p_gateway.recvline()
if pow.startswith(b"== proof-of-work: enabled =="):
    p_gateway.recvline()
    p_gateway.recvline()
    challenge = p_gateway.recvline().decode().split(" ")[-1]
    p_gateway.recvuntil("Solution? ")
    p_gateway.sendline(solve_challenge(challenge))

# Get the IP and port of the instance
p_gateway.recvuntil("ip = ")
ip = p_gateway.recvuntil("\n").decode().strip()
p_gateway.recvuntil("port = ")
port = int(p_gateway.recvuntil("\n").decode().strip())

# Helper to start the bot (which has the flag)
# (optionally, you can start the bot with a fake flag for debugging)
def start_bot(fake_flag=None):
    p_gateway.recvuntil("Choice: ")

    if fake_flag is not None:
        p_gateway.sendline("2")
        p_gateway.recvuntil(":")
        p_gateway.sendline(fake_flag)
    else:
        p_gateway.sendline("1")

    p_gateway.recvuntil("Bot spawned")

p = remote(ip, port)

# Start bot with real flag
start_bot()

# ** your really great solution goes here **


p.interactive()