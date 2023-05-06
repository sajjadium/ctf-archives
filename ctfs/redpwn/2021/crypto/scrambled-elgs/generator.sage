#!/usr/bin/env sage
import secrets
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes
from sage.combinat import permutation

n = 25_000
Sn = SymmetricGroup(n)

def pad(M):
    padding = long_to_bytes(secrets.randbelow(factorial(n)))
    padded = padding[:-len(M)] + M
    return bytes_to_long(padded)

#Prepare the flag
with open('flag.txt','r') as flag:
    M = flag.read().strip().encode()
m = Sn(permutation.from_rank(n,pad(M)))

#Scramble the elgs
g = Sn.random_element()
a = secrets.randbelow(int(g.order()))
h = g^a
pub = (g, h)

#Encrypt using scrambled elgs
g, h = pub
k = secrets.randbelow(n)
t1 = g^k
t2 = m*h^k
ct = (t1,t2)

#Provide public key and ciphertext
with open('output.json','w') as f:
	json.dump({'g':str(g),'h':str(h),'t1':str(t1),'t2':str(t2)}, f)
