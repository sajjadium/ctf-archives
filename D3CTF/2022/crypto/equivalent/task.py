from collections import namedtuple
from Crypto.Util import number
from Crypto.Random import random


PublicKey = namedtuple('PublicKey', ['a'])
SecretKey = namedtuple('SecretKey', ['s', 'e', 'p'])



def keygen(sbit, N):
    s_ = [random.getrandbits(sbit) | 1 for _ in range(N)]

    pbit = sum(s_).bit_length() + 1
    p = number.getPrime(pbit)
    while not (sum(s_) < p < 2*sum(s_)):
        p = number.getPrime(pbit)
    e = random.randint(p//2, p-1)

    a_ = [e*s_i % p for s_i in s_]

    assert 2**N > max(a_)

    pk = PublicKey(a_)
    sk = SecretKey(s_, e, p)

    return (pk, sk)


def enc(m, pk):
    assert 0 <= m < 2
    n = len(pk.a)
    r_ = [random.getrandbits(1) for _ in range(n-1)]
    r_n = (m - sum(r_)) % 2
    r_.append(r_n)
    c = sum(a_i*r_i for a_i, r_i in zip(pk.a, r_))
    return c


def dec(c, sk):
    e_inv = number.inverse(sk.e, sk.p)
    m = (e_inv * c % sk.p) % 2
    return m


def encrypt(msg, pk):
    bits = bin(number.bytes_to_long(msg))[2:]
    cip = [enc(m, pk) for m in map(int, bits)]
    return cip


def decrypt(cip, sk):
    bits = [dec(c, sk) for c in cip]
    msg = number.long_to_bytes(int(''.join(map(str, bits)), 2))
    return msg


if __name__ == "__main__":
    from secret import FLAG

    pk, sk = keygen(sbit=80, N=100)

    msg = FLAG.removeprefix(b"d3ctf{").removesuffix(b"}")
    cip = encrypt(msg, pk)

    assert msg == decrypt(cip, sk)

    with open("data.txt", 'w') as f:
        f.write(f"pk = {pk}\n")
        f.write(f"cip = {cip}\n")
