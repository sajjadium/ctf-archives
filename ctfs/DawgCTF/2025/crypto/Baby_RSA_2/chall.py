from Crypto.Util.number import *
from secret import flag

# This is my stuff! Don't look at it
p = getPrime(512)
q = getPrime(512)
N = p * q

e_priv = 0x10001
phi = (p - 1) * (q - 1)

d_priv = inverse(e_priv, phi)

m = bytes_to_long(flag)
c = pow(m, e_priv, N)

# This is your stuff!
e_pub = getPrime(16)
    
d_pub = inverse(e_pub, phi) 

print(f"e = {e_pub}")
print(f"d = {d_pub}")
print(f"N = {N}")
print(f"c = {c}")
