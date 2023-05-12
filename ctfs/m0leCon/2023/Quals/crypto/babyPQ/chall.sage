from sage.crypto.boolean_function import BooleanFunction, random_boolean_function
from Crypto.Cipher import ChaCha20
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes, bytes_to_long
import os

def create_sbox(m, n, p, priv):
    Bs = []

    for _ in range(n-1):
        B = random_boolean_function(m)
        Bs.append(B)
    
    last_bf = []

    for i in range(2^m):
        val = sum([priv[j] * int(Bs[j](i)) for j in range(n-1)]) % 2
        if random() < p:
            last_bf.append(val)
        else:
            last_bf.append(1-val)

    Bs.append(BooleanFunction(last_bf))

    Bs = matrix([[int(x) for x in B.truth_table()] for B in Bs]).transpose()
    S = []

    for B in Bs:
        S.append(sum([B[i]*2^i for i in range(n)]))
    
    return S

def gen_keypair(m, n, p):
    private_key = [randint(0,1) for _ in range(n-1)]
    private_key.append(1)
    SBoxes = []

    for _ in range(6):
        SBoxes.append(create_sbox(m, n, p, private_key))
    
    return SBoxes, private_key

def expand_key(key, rounds):
    ks = [key]
    
    for _ in range(rounds-1):
        cipher = ChaCha20.new(key = bytes([_])*32, nonce = b"\x00"*8)
        ks.append(cipher.encrypt(ks[-1]))
    
    return [bytes_to_long(k) for k in ks]

def f(p, sboxes):
    p = [(p>>(8*i)) & 0xFF for i in range(6)]
    res = 0
    for i in range(6):
        res ^^= sboxes[i][p[i]]
    return res

def feistel_encrypt(pt, key, sboxes):
    ks = expand_key(key, 8)
    l, r = bytes_to_long(pt[:6]), bytes_to_long(pt[6:])
    
    for i in range(8):
        l, r = r, l ^^ f(r ^^ ks[i], sboxes)
    
    return long_to_bytes(l) + long_to_bytes(r)

def encrypt(pt, public_key):
    tmp_key = os.urandom(8)
    ad = []
    
    for _ in range(1024):
        tmp_pt = os.urandom(12)
        tmp_ct = feistel_encrypt(tmp_pt, tmp_key, public_key)
        ad.append((tmp_pt.hex(), tmp_ct.hex()))
    
    pt = pad(pt, 12)
    pt = [pt[i:i+12] for i in range(0, len(pt), 12)]

    c = b''.join([feistel_encrypt(p, tmp_key, public_key) for p in pt]).hex()

    return (c, ad)

def decrypt(ct, private_key):
    # :)
    pass

public_key, private_key = gen_keypair(8, 48, 0.97)
flag = open("flag.txt", "rb").read()
enc = encrypt(flag, public_key)
print(f"{public_key = }")
print(f"{enc = }")