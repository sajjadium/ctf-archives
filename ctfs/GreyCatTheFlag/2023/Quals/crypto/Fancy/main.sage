from Crypto.Util.number import getPrime
from secrets import randbits
from hashlib import shake_256

FLAG = b'???'

p = 2^29 - 33

F.<x,y> = GF(p)[]
G.<x,y> = F.quotient(F.ideal([x^3 - y^2 + 1, y^7 - 11]))

def xor(a, b):
    return bytes([i ^^ j for i, j in zip(a,b)])

def encrypt_flag(s):
    secret = b",".join(map(lambda x : str(x).encode(), s.lift().coefficients()))
    key = shake_256(secret).digest(len(FLAG))
    return xor(key, FLAG)

g = 1 + x + y

a = randbits(1024); A = g^a
b = randbits(1024); B = g^b
S = A^b

f = open("output.txt", 'w')

f.write(f"c = {encrypt_flag(S).hex()}\n")
f.write(f"A = {A}\n")
f.write(f"B = {B}\n")
