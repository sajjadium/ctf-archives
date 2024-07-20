from sage.all import *
import os
from Crypto.Cipher import AES
from hashlib import sha512

proof.all(False)
p = 0x7AADA0BA1C05D63803BA6BCE66CB6BC091C7ADA62B5CB5BC9F924B528FC113971D4BC54C7FAF3C146ADEB0548BFB9258DFF316741266B802DD7A2F46F77593BAD983E6DF394C1519E8DB0130289FA5A9C628E3ABCE58C63B3379DB7088AAC7A40B63776959774B1B57B8FD316C650AE3C012A91EE653477443446050438A99E79B89B69745BD1918EECB08A0C9D45EF3C61639137F24D979FF380D65C7ABD08785F1AF99729A62F3690747AEC4CCBDA99BAE6E990A0FEFF6F1AB9ABEAFE7FB5BDDB8471C607DEC16198A2AE7776C56B5B6CA24B4C0A2441A047A18EB23302B46CC49ADFF6188FC97C886D5BF67B4B0EFF56762C4E48AAD3F02E7CFE8AA157FB1789B1
F = GF(p)


def magic_op(x, n):
    r0, r1 = 1, x
    for b in f"{n:b}":
        if b == "0":
            r1 = 2 * r0 * r1 - x
            r0 = 2 * r0**2 - 1
        else:
            r0 = 2 * r0 * r1 - x
            r1 = 2 * r1**2 - 1
    return r0


if __name__ == "__main__":
    with open("flag.txt", "rb") as f:
        flag = f.read().strip()
    h = int(sha512(flag).hexdigest(), 16)

    magic_pi = magic_op(F(314159), h)
    magic_e = magic_op(F(271828), h)

    key = os.urandom(16)
    k = F(int.from_bytes(key, "big"))
    fake_k = [F.random_element() for _ in range(63)]
    fake_k += [k - sum(fake_k)]
    obfuscated_keys = [magic_op(k, h) for k in fake_k]

    cipher = AES.new(key, AES.MODE_CTR)
    ct = cipher.encrypt(flag)
    iv = cipher.nonce

    print(f"{magic_pi = }")
    print(f"{magic_e = }")
    print(f"{obfuscated_keys = }")
    print(f"{ct = }")
    print(f"{iv = }")
