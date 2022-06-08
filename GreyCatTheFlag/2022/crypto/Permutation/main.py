from secrets import randbits
from hashlib import shake_256
import random
import perm

FLAG = <REDACTED>

def encrypt(key : str) -> str:
    otp = shake_256(key.encode()).digest(len(FLAG))
    return xor(otp, FLAG).hex()

def xor(a : bytes, b : bytes) -> bytes:
    return bytes([ x ^ y for x, y in zip(a, b)])

n = 5000
h = 2048

arr = [i for i in range(n)]
random.shuffle(arr)

g = perm.Perm(arr)
a = randbits(h); b = randbits(h)
A = g ** a; B = g ** b
S = A ** b
key = str(S)

print(f"g = [{g}]"); print(f"A = [{A}]"); print(f"B = [{B}]"); 

print(f"c = {encrypt(key)}")