from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
import random

n = 42
m = 20
G = AlternatingGroup(m)

pub_a = [G.random_element() for _ in range(n)]
pub_b = [G.random_element() for _ in range(n)]

eps_a = [random.choice([1,-1]) for _ in range(n)]
eps_b = [random.choice([1,-1]) for _ in range(n)]

A = prod([x^e for x,e in zip(pub_a, eps_a)])
B = prod([x^e for x,e in zip(pub_b, eps_b)])

abar = [A^(-1) * x * A for x in pub_b]
bbar = [B^(-1) * x * B for x in pub_a]

print(pub_a)
print(pub_b)
print(abar)
print(bbar)

K = A^(-1)*B^(-1)*A*B
shared = "_".join(str(K(i)) for i in range(1,m+1))
dig = sha256(shared.encode()).digest()
key = dig[:16]
iv = dig[16:]
aes = AES.new(key, AES.MODE_CBC, iv=iv)
with open("flag.txt", "rb") as f:
    flag = f.read()
flag_enc = aes.encrypt(pad(flag,16))
print(flag_enc.hex())
