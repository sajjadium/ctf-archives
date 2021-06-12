import pwn
import hashlib
import itertools
import string

"""
This is an example showing how to connect to the challenge with pwntools,
proof-of-work solver included.
"""


def solve_pow(io):
    suffix = io.recvlineS().strip().split(" = ")[-1]
    h = io.recvlineS().strip().split(" = ")[-1]
    prefix_len = int(io.recvuntilS(": ").lstrip("[*] Give me the ").split()[0])
    print("[*] Solving PoW: sha256({}{}) == {}".format("?" * prefix_len, suffix, h))

    pool = string.ascii_letters + string.digits
    for p in itertools.product(pool, repeat=prefix_len):
        prefix = "".join(p)
        if hashlib.sha256((prefix + suffix).encode()).hexdigest() == h:
            print("[+] prefix = " + prefix)
            io.sendline(prefix)
            return
    else:
        print("[-] Solution not found")


io = pwn.remote("localhost", 7000)
solve_pow(io)
io.interactive()
