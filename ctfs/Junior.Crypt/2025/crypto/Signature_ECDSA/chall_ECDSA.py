from ecdsa import SECP256k1
import hashlib
from random import randint
from mySecret import d  # d in range(1,n) - my Private Key

# =============================================
# 0. Elliptic Curve SECP256k1 Parameters
# =============================================
curve = SECP256k1
G = curve.generator  # Base Point
n = curve.order      # Subgroup Order

# =============================================
# 1. Generating Keys and Messages
# =============================================
Q = d * G                     # my Public Key

m1 = b"Hello, world!"
m2 = b"Goodbye, world!"

h1 = int(hashlib.sha256(m1).hexdigest(), 16) % n
h2 = int(hashlib.sha256(m2).hexdigest(), 16) % n

# =============================================
# 2. Generating signatures 
# =============================================
k = randint(1, n - 1)  
R = k * G
r = R.x() % n

# Signature for m1
s1 = (pow(k, -1, n) * (h1 + r * d)) % n

# Signature for m2
s2 = (pow(k, -1, n) * (h2 + r * d)) % n  

print(f"\n[Signature 1]\nr1 = {hex(r)}\ns1 = {hex(s1)}\nh1 = {hex(h1)}\n")
print(f"[Signature 2]\nr2 = {hex(r)}\ns2 = {hex(s2)}\nh2 = {hex(h2)}")

====

[Signature 1]
r1 = 0xe37ce11f44951a60da61977e3aadb42c5705d31363d42b5988a8b0141cb2f50d
s1 = 0xdf88df0b8b3cc27eedddc4f3a1ecfb55e63c94739e003c1a56397ba261ba381d
h1 = 0x315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3

[Signature 2]
r2 = 0xe37ce11f44951a60da61977e3aadb42c5705d31363d42b5988a8b0141cb2f50d
s2 = 0x2291d4ab9e8b0c412d74fb4918f57580b5165f8732fd278e65c802ff8be86f61
h2 = 0xa6ab91893bbd50903679eb6f0d5364dba7ec12cd3ccc6b06dfb04c044e43d300
