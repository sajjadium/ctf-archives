from secret import key, flag
from constants import *

def pad(a: list, length: int = 54) -> list:
    return a + [0] * (length - len(a))

def int_to_bytes(a: int, length: int = 0, order: str = "little") -> bytes:
    if length < 1: length = (a.bit_length() + 7) // 8
    return a.to_bytes(length, order)

def bytes_to_int(a: bytes, order: str = "little") -> int:
    return int.from_bytes(a, order)

def int_to_trits(a: int) -> list:
    out = []
    while a:
        a, temp = divmod(a, 3)
        out.append(temp)
    return out

def trits_to_int(a: list) -> int:
    return sum(j * 3 ** i for i, j in enumerate(a))

def trits_to_bytes(a: list) -> bytes:
    return int_to_bytes(trits_to_int(a))

def bytes_to_trits(a: bytes, length: int = 54) -> list:
    return pad(int_to_trits(bytes_to_int(a)), length)

def xor(a: list, b: list) -> list:
    return [(i + j) % 3 for i, j in zip(a, b)]

def uxor(a: list, b: list) -> list:
    return [(i - j) % 3 for i, j in zip(a, b)]

def rot(a: list, n: int) -> list:
    return a[n:] + a[:n]

def perm(a: list, pbox: tuple) -> list:
    return [a[i] for i in pbox]

def expand(key: list) -> list[list]:
    assert len(key) == 54
    key = perm(key, KEY_PERM1)
    L, R = key[:24], key[24:]
    out = []

    for s in SHIFTS:
        L = rot(L, s)
        R = rot(R, s)
        out.append(perm(L + R, KEY_PERM2))
    
    return out

def feistel(inp: list, key: list) -> list:
    assert len(inp) == 27 and len(key) == 36
    inp = perm(inp, EXP_PERM)
    inp = xor(inp, key)
    out = []

    for i in range(9):
        chunk = inp[i * 4:i * 4 + 4]
        temp = pad(int_to_trits(SBOX[i][trits_to_int(chunk)]), 3)
        out.extend(temp)
    
    return perm(out, FEISTEL_PERM)

def enc(inp: list, key: list) -> list:
    assert len(inp) == len(key) == 54
    inp = perm(inp, INIT_PERM)
    L, R = inp[:27], inp[27:]
    key = expand(key)
    
    L = xor(L, feistel(R, key[0]))
    for k in key[1:]:
        L, R = R, L
        L = xor(L, feistel(R, k))

    return perm(L + R, FINAL_PERM)

def dec(inp: list, key: list) -> list:
    assert len(inp) == len(key) == 54
    inp = perm(inp, INIT_PERM)
    L, R = inp[:27], inp[27:]
    key = expand(key)[::-1]
    
    L = uxor(L, feistel(R, key[0]))
    for k in key[1:]:
        L, R = R, L
        L = uxor(L, feistel(R, k))
    
    return perm(L + R, FINAL_PERM)

def encrypt(inp: bytes, key: bytes) -> bytes:
    inp = bytes_to_trits(inp)
    assert len(inp) <= 54, "Message information will be lost. Shorten or break the message into chunks."
    key = bytes_to_trits(key)
    return trits_to_bytes(enc(inp, key))

def decrypt(inp: bytes, key: bytes) -> bytes:
    inp = bytes_to_trits(inp)
    assert len(inp) <= 54, "Message information will be lost. Shorten or break the message into chunks."
    key = bytes_to_trits(key)
    return trits_to_bytes(dec(inp, key))

# 100% another benchmark
def main() -> None:
    import random, itertools, hashlib, time

    start = time.time()

    # Was gonna encrypt under D3S but willwam said no. ;-; (have fun bruting)
    assert b"corctf{" in flag
    out = [str(bytes(i ^ j for i, j in zip(hashlib.sha512(key).digest(), flag)))]

    key2 = bytes_to_trits(key)
    msg = [random.randint(0, 2) for _ in range(54)]
    mask = [0, 4, 5, 20, 22, 35, 37, 38, 45] # I promise nothing weird happens after 4 rounds.

    for i in itertools.product(range(3), repeat=len(mask)):
        for a, b in zip(i, mask): msg[b] = a
        out.append(str((trits_to_bytes(msg), trits_to_bytes(enc(msg, key2)))))

    end = time.time()
    out.append(f"This took: {end - start} seconds.")

    with open("./output.txt", "w+") as f:
        f.write("\n".join(out))

if __name__ == "__main__":
    main()
