from Crypto.Util.number import getPrime, bytes_to_long
from math import prod

ps = [getPrime(512) for _ in range(5)]
N1 = prod(ps[:3])
N2 = prod(ps[2:])
e = 0x10001

with open("flag.txt", "rb") as f:
    flag = bytes_to_long(f.read())

c1 = pow(flag, e, N1)
c2 = pow(flag, e, N2)

with open("output.txt", "w") as f:
    f.write(f"{N1 = }\n")
    f.write(f"{N2 = }\n")
    f.write(f"{c1 = }\n")
    f.write(f"{c2 = }\n")
