load("util.sage")
import hashlib, secrets
from Crypto.Cipher import AES
from tqdm import tqdm

flag = b"uiuctf{REDACTED}"
steps = 32

g, a = initial_edge()
path = [_serialize_j(j_invariant(g))]

for i in tqdm(range(steps)):
    edges = sorted(forward_edges(g, a, True), key=lambda e: str(j_invariant(e[0])))
    g, a = edges[secrets.randbelow(q - 1)]
    path.append(_serialize_j(j_invariant(g)))

    if i + 1 < steps:
        g, a = secrets.choice(forward_edges(g, a))
        path.append(_serialize_j(j_invariant(g)))

key = hashlib.sha256(b"".join(path)).digest()
iv = secrets.token_bytes(AES.block_size)
ct = AES.new(key, AES.MODE_CTR, nonce=b"", initial_value=iv).encrypt(flag)
print("steps =", steps)
print("isogeny_degree =", 2*steps)
print("j =", j_invariant(g))
print("iv =", iv.hex())
print("ct =", ct.hex())
