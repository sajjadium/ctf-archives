from Crypto.Cipher import AES
from hashlib import sha256

proof.all(False)
# fmt: off
ls = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 929]
# fmt: on
p = 4 * product(ls) - 1
F = GF(p)
E0 = EllipticCurve(F, [1, 0])
G = E0.gen(0)
base = (E0, G)


def keygen():
    return [randint(-1, 1) for _ in range(len(ls))]


def exchange(pub, priv):
    E, G = pub
    es = priv[:]
    while any(es):
        s = +1 if randint(0, 1) else -1
        E.set_order(p + 1)
        P = E.random_point()
        k = prod(l for l, e in zip(ls, es) if sign(e) == s)
        P *= (p + 1) // k
        for i, (l, e) in enumerate(zip(ls, es)):
            if sign(e) != s:
                continue
            Q = k // l * P
            if not Q:
                continue
            Q.set_order(l)
            phi = E.isogeny(Q)
            E, P = phi.codomain(), phi(P)
            G = phi(G)
            es[i] -= s
            k //= l
    return E, G


def serialize_pub(pub):
    E, G = pub
    return (E.a4(), E.a6(), G[0], G[1])


with open("flag.txt", "rb") as f:
    flag = f.read().strip()

priv_alice = keygen()
priv_bob = keygen()
pub_alice = exchange(base, priv_alice)
pub_bob = exchange(base, priv_bob)
shared_1 = exchange(pub_alice, priv_bob)
shared_2 = exchange(pub_bob, priv_alice)
assert shared_1 == shared_2

shared_secret = int(shared_1[0].j_invariant() + shared_1[1][0])
key = sha256(str(shared_secret).encode()).digest()
cipher = AES.new(key, AES.MODE_CTR)
ct = cipher.encrypt(flag)
iv = cipher.nonce

base_ser = serialize_pub(base)
pub_alice_ser = serialize_pub(pub_alice)
pub_bob_ser = serialize_pub(pub_bob)

print(f"{base_ser = }")
print(f"{pub_alice_ser = }")
print(f"{pub_bob_ser = }")
print(f"{ct = }")
print(f"{iv = }")
