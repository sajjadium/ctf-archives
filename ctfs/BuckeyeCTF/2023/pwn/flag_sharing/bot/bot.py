import sys

if sys.argv[1] == "":
    with open("flag.txt", "r") as f:
        flag = f.read()
else:
    flag = sys.argv[1]

flag = int.from_bytes(flag.encode(), "little")

from pwn import *

p = remote("chal", 5000)
p.recvuntil(b"----")
p.recvline()
p.recvuntil(b"----")
p.recvline()

while flag != 0:
    match flag & 3:
        case 0:
            p.sendline(b"W")
        case 1:
            p.sendline(b"A")
        case 2:
            p.sendline(b"S")
        case 3:
            p.sendline(b"D")

    p.recvuntil(b"----")
    p.recvline()
    p.recvuntil(b"----")
    p.recvline()
    print(hex(flag))

    flag = flag >> 2
    time.sleep(0.25)
