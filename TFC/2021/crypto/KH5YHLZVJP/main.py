import base64
import random
from pwn import xor
from secret import flag

with open("c.out", "w") as f:
    for _ in range(4):
        x = random.getrandbits(4096)
        f.write(str(x) + "\n")
    x = random.getrandbits(4096)
    x = xor(flag, str(x)[:512])
    secret = base64.b64encode(x).decode("utf-8")
    f.write("SECRET: " + secret)

