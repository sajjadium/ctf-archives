from Crypto.Util.number import long_to_bytes, getPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
from secrets import randbelow
from random import sample

p = getPrime(256)
a = randbelow(p)
b = randbelow(p)
s = randbelow(p)

def f(s):
    return (a * s + b) % p

jumps = sample(range(3, 25), 12)
output = [s]
for jump in jumps:
    for _ in range(jump):
        s = f(s)
    output.append(s)

print(jumps)
print(output)

flag = open("flag.txt", "rb").read()
key = sha256(b"".join([long_to_bytes(x) for x in [a, b, p]])).digest()[:16]
iv = long_to_bytes(randbelow(2**128))

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
print(iv.hex() + cipher.encrypt(pad(flag, 16)).hex())