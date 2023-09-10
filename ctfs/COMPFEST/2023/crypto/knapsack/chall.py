from collections import namedtuple
import random
from Crypto.Util.number import isPrime, GCD
from secret import message, key_size

PrivateKey = namedtuple("PrivateKey", "W q r")
PublicKey = namedtuple("PublicKey", "B")

def to_bits(m):
    _bin = lambda b: [1 if b & (1 << n) else 0 for n in range(7)]
    return sum([_bin(b) for b in m], [])


def to_bytes(bits):
    _byte = lambda b: sum([b[i] << i for i in range(7)])
    return bytes([_byte(bits[i : i + 7]) for i in range(0, len(bits), 7)])


def pad(m):
    return m + b"\x00" * (-len(m) % (key_size // 7))


def unpad(m):
    return m.rstrip(b"\x00")


def gen_private_key(key_size):
    W = []
    s = 6969

    # generate W
    for _ in range(key_size):
        w_i = random.randint(s + 1, 2 * s)
        assert w_i > sum(W)
        W.append(w_i)
        s += w_i

    # generate q
    while True:
        q = random.randint(2 * s, 32 * s)
        if isPrime(q):
            break

    # generate r
    r = random.randint(s + 1, q - 1)

    assert q > sum(W)
    assert GCD(q, r) == 1
    return PrivateKey(W, q, r)


def gen_public_key(private_key):
    B = []
    for w_i in private_key.W:
        B.append((private_key.r * w_i) % private_key.q)
    return PublicKey(B)


def encrypt(msg, public_key):
    msg_bit = to_bits(pad(msg))
    key_size = len(public_key.B)
    enc = []
    for i in range(0, len(msg_bit), key_size):
        enc.append(sum([msg_bit[i + j] * public_key.B[j] for j in range(key_size)]))
    return enc


def decrypt(enc, private_key):
    dec = []
    for c in enc:
        c_ = (c * pow(private_key.r, -1, private_key.q)) % private_key.q
        bits = []
        for w_i in reversed(private_key.W):
            if c_ >= w_i:
                bits.append(1)
                c_ -= w_i
            else:
                bits.append(0)
        dec += bits[::-1]
    return unpad(to_bytes(dec))

private_key = gen_private_key(key_size)
public_key = gen_public_key(private_key)
enc = encrypt(message, public_key)
dec = decrypt(enc, private_key)


assert dec == message

with open("output.txt", "w") as f:
    # f.write(f"B = {public_key.B}\n")
    f.write(f"enc = {enc}\n")
    f.write(f"{message[:1194].decode()}")