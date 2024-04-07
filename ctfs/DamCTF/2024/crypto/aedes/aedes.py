#!/usr/local/bin/python3

from functools import reduce, partial
import operator
import secrets

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def xor(*bs):
    return bytes(reduce(operator.xor, bb) for bb in zip(*bs, strict=True))

def expand_k(k):
    sched = []
    for i in range(7):
        subkey = F(k, i.to_bytes(16))
        sched[i:i] = [subkey, subkey]

    sched.insert(7, F(k, (7).to_bytes(16)))
    return sched


def F(k, x):
    f = Cipher(algorithms.AES(k), modes.ECB()).encryptor()
    return f.update(x) + f.finalize()


def enc(k, m):
    subkeys = expand_k(k)
    left, right = m[:16], m[16:]

    for i in range(15):
        old_right = right
        right = xor(left, F(subkeys[i], right))
        left = old_right
        
    return left + right


print("Introducing AEDES, the result of taking all of the best parts of AES and DES and shoving them together! It should be a secure block cipher but proofs are hard so I figured I'd enlist the help of random strangers on the internet! If you're able to prove me wrong you might get a little prize :)")

key = secrets.token_bytes(16)

with open("flag", "rb") as f:
    flag = f.read(32)

assert len(flag) == 32
flag_enc = enc(key, flag)

print("Since I'm so confident in the security of AEDES, here's the encrypted flag. Good luck decrypting it without the key :)")
print(flag_enc.hex())

for _ in range(5):
    pt_hex = input("Your encryption query (hex): ")
    try:
        pt = bytes.fromhex(pt_hex)
        assert len(pt) == 32
    except (ValueError, AssertionError):
        print("Make sure your queries are 32 bytes of valid hex please")
        continue

    ct = enc(key, pt)
    print("Result (hex):", ct.hex())
