from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
from ecdsa.curves import SECP256k1
from ecdsa.ellipticcurve import Point
from hashlib import sha256
from secrets import randbelow

C = SECP256k1
G = C.generator
n = C.order

def sign(d, Q, h, k):
    R = k * G
    r = R.x()
    e = int.from_bytes(sha256(r.to_bytes(32, 'big') + Q.x().to_bytes(32, 'big') + h).digest(), 'big') % n
    s = (k + e * d) % n
    return r, s

def verify(Q, h, r, s):
    e = int.from_bytes(sha256(r.to_bytes(32, 'big') + Q.x().to_bytes(32, 'big') + h).digest(), 'big') % n
    sG = (s * G).to_affine()
    eQ = (e * Q).to_affine()
    Rp = Point(C.curve, sG.x(), sG.y()) + Point(C.curve, eQ.x(), (-eQ.y()) % C.curve.p())
    return Rp.x() == r

def lcg(a, c, m, x):
    while True:
        x = (a * x + c) % m
        yield x

if __name__ == "__main__":
    d = randbelow(n)
    Q = d * G
    p = getPrime(256)
    a, c, seed = [randbelow(p) for _ in range(3)]
    lcg_gen = lcg(a, c, p, seed)
    msgs = [
        b"The true sign of intelligence is not knowledge but imagination.",
        b"In the middle of difficulty lies opportunity.",
        b"I have no special talent. I am only passionately curious.",
        b"The only source of knowledge is experience.",
        b"Logic will get you from A to B. Imagination will take you everywhere.",
        b"Life is like riding a bicycle. To keep your balance, you must keep moving.",
        b"Strive not to be a success, but rather to be of value.",
        b"Weakness of attitude becomes weakness of character.",
        b"Peace cannot be kept by force; it can only be achieved by understanding.",
        b"It's not that I'm so smart, it's just that I stay with problems longer."
    ]
    sigs = []

    for m in msgs:
        h = sha256(m).digest()
        st = next(lcg_gen)
        k = st >> 128
        r, s = sign(d, Q, h, k)
        assert verify(Q, h, r, s)
        sigs.append((r, s))

    print(f"Q = ({Q.x()}, {Q.y()})")
    print(f"sigs = {sigs}")

    flag = b"CRHC{fake_flag}"
    key = sha256(d.to_bytes(32, 'big')).digest()[:16]
    aes = AES.new(key, AES.MODE_GCM)
    enc_flag, tag = aes.encrypt_and_digest(flag)
    nonce = aes.nonce

    print(f"\nenc_flag = {enc_flag.hex()}")
    print(f"nonce = {nonce.hex()}")
    print(f"tag = {tag.hex()}")