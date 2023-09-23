from sage.all import *
from flag import flag
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from random import SystemRandom
random = SystemRandom()
# Secp256k1
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a = 0
b = 7
E = EllipticCurve(GF(p), [a, b])
G = E.gens()[0]
order = E.order()
Fn = GF(order)
d = random.randint(1, order)
hd = hex(d)[2:]
if len(hd) % 2 == 1:
    hd = '0' + hd
key = bytes.fromhex(hd)
iv = random.randbytes(16)
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
flag = flag.encode()
flag = pad(flag, 16)
c = cipher.encrypt(flag)
print(f"iv = '{iv.hex()}'")
print(f"c = '{c.hex()}'")


def gen_nonce(): return 2**128*(d % (2**128)) + (d >> 128)


nonce = gen_nonce()
msg = random.randbytes(32)
z = int.from_bytes(msg, 'big')
# sign
public = d*G
r = Fn((nonce*G).xy()[0])
s = Fn(nonce)**(-1) * (z + r*d)

print(f"public = {public.xy()}")
print(f"{s = }")
print(f"{r = }")
print(f"msg = '{msg.hex()}'")

inv_s = pow(int(s), -1, order)
u1 = int(z*int(inv_s)) % order
u2 = int(r*int(inv_s)) % order
P = u1*G + u2*public
P = P.xy()[0]
assert int(P) == int(r), "Signature is invalid??!??!?!?!??!?!?!"