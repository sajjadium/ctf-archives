#!/usr/bin/env python3
import struct, hashlib, random, os
from Crypto.Cipher import AES

n = 256
q = 11777
w = 8

################################################################

sample = lambda rng: [bin(rng.getrandbits(w)).count('1') - w//2 for _ in range(n)]

add = lambda f,g: [(x + y) % q for x,y in zip(f,g)]

def mul(f,g):
    r = [0]*n
    for i,x in enumerate(f):
        for j,y in enumerate(g):
            s,k = divmod(i+j, n)
            r[k] += (-1)**s * x*y
            r[k] %= q
    return r

################################################################

def genkey():
    a = [random.randrange(q) for _ in range(n)]
    rng = random.SystemRandom()
    s,e = sample(rng), sample(rng)
    b = add(mul(a,s), e)
    return s, (a,b)

center = lambda v: min(v%q, v%q-q, key=abs)
extract = lambda r,d: [2*t//q for u,t in zip(r,d) if u]

ppoly = lambda g: struct.pack(f'<{n}H', *g).hex()
pbits = lambda g: ''.join(str(int(v)) for v in g)
hbits = lambda g: hashlib.sha256(pbits(g).encode()).digest()
mkaes = lambda bits: AES.new(hbits(bits), AES.MODE_CTR, nonce=b'')

def encaps(pk):
    seed = os.urandom(32)
    rng = random.Random(seed)
    a,b = pk
    s,e = sample(rng), sample(rng)
    c = add(mul(a,s), e)
    d = add(mul(b,s), e)
    r = [int(abs(center(2*v)) > q//7) for v in d]
    bits = extract(r,d)
    return bits, (c,r)

def decaps(sk, ct):
    s = sk
    c,r = ct
    d = mul(c,s)
    return extract(r,d)

################################################################

if __name__ == '__main__':

    while True:
        sk, pk = genkey()
        dh, ct = encaps(pk)
        if decaps(sk, ct) == dh:
            break

    print('pk[0]:', ppoly(pk[0]))
    print('pk[1]:', ppoly(pk[1]))

    print('ct[0]:', ppoly(ct[0]))
    print('ct[1]:', pbits(ct[1]))

    flag = open('flag.txt').read().strip()
    print('flag: ', mkaes([0]+dh).encrypt(flag.encode()).hex())

    for _ in range(2048):
        c = list(struct.unpack(f'<{n}H', bytes.fromhex(input())))
        r = list(map('01'.index, input()))
        if len(r) != n or sum(r) < n//2: exit('!!!')

        bits = decaps(sk, (c,r))

        print(mkaes([1]+bits).encrypt(b'hxp<3you').hex())

