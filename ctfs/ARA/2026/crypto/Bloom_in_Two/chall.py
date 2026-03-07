from Crypto.Util.number import *
import hashlib, os, random, signal

flag = open("flag.txt", "rb").read().strip()

N_BITS = 512

def bloom_in_two(nbits, growth, hm, hm1, hm2):
    seed_bits = int(nbits * growth)
    d_bits = int(nbits * hm)
    m = int(nbits * hm1)
    l = int(nbits * hm2)
    hehe = d_bits - m - l
    if hehe <= 0:
        raise ValueError("?")

    a_bits = (nbits // 2) - seed_bits - 1
    if a_bits <= 32:
        raise ValueError("?")

    e_low = int(0.70 * nbits)
    e_high = int(0.74 * nbits)

    while True:
        g = getPrime(seed_bits)

        while True:
            a = random.getrandbits(a_bits)
            if a < (1 << (a_bits - 1)):
                continue
            p = 2 * g * a + 1
            if isPrime(p):
                break

        while True:
            b = random.getrandbits(a_bits)
            if b < (1 << (a_bits - 1)) or b == a:
                continue
            if GCD(a, b) != 1:
                continue
            q = 2 * g * b + 1
            if isPrime(q):
                break

        N = p * q
        lcm = 2 * g * a * b
        d = getPrime(d_bits)
        if GCD(d, lcm) != 1:
            continue

        e = inverse(d, lcm)
        if not (e_low <= e.bit_length() <= e_high):
            continue

        d_hi = d >> (hehe + l)
        d_lo = d & ((1 << l) - 1)

        return {
            "N": N,
            "e": e,
            "d": d,
            "d_bits": d_bits,
            "m": m,
            "l": l,
            "hehe": hehe,
            "d_hi": d_hi,
            "d_lo": d_lo,
        }

def gen(n, m, coeff_bits, mod_bits, big_bits, shift):
    q = getPrime(mod_bits)
    B = [random.randrange(1 << (big_bits - 1), 1 << big_bits) for _ in range(n)]

    rows = []
    while len(rows) < m:
        coeffs = [random.randint(-(1 << coeff_bits), 1 << coeff_bits) for _ in range(n)]
        if all(c == 0 for c in coeffs):
            continue
        t = sum(c * b for c, b in zip(coeffs, B)) % q
        r = t >> shift
        rows.append((coeffs, r))

    digest = hashlib.sha256(",".join(str(x) for x in B).encode()).hexdigest()
    return q, rows, digest

def derive(salt_hex, idx, token, n, coeff_bits, shift):
    seed = f"{salt_hex}|{idx}|{token}".encode()
    stream = hashlib.shake_256(seed).digest(4 * n + 16)
    span = 1 << coeff_bits

    coeffs = []
    ptr = 0
    for _ in range(n):
        x = int.from_bytes(stream[ptr : ptr + 4], "big")
        ptr += 4
        coeffs.append((x % (2 * span + 1)) - span)

    pad_raw = int.from_bytes(stream[ptr : ptr + 8], "big")
    mask_raw = int.from_bytes(stream[ptr + 8 : ptr + 16], "big")
    pad = pad_raw & ((1 << shift) - 1)
    mask = mask_raw & ((1 << 48) - 1)
    return coeffs, pad, mask

def main():
    inst = bloom_in_two(N_BITS, 0.28, 0.25, 0.15, 0.0)

    print("[phase 1]")
    print("N =", inst["N"])
    print("e =", inst["e"])
    print("d_hi =", inst["d_hi"])
    print("d_lo =", inst["d_lo"])

    for i in range(3):
        print(f"round {i + 1}/{3}")
        target_str = os.urandom(16).hex()
        m = bytes_to_long(target_str.encode())
        ct_m = pow(m, inst["e"], inst["N"])
        print("ct_m =", ct_m)
        guess = int(input("guess = ").strip())
        if guess != m:
            print("wrong")
            os._exit(0)
        print("ok")

    print("[phase 2]")
    shift = 8
    q = getPrime(256)
    B = [random.randrange(1, q) for _ in range(10)]
    digest = hashlib.sha256(",".join(str(x) for x in B).encode()).hexdigest()
    salt_hex = os.urandom(12).hex()
    print("q =", q)
    print("shift =", shift)
    print("n =", 10)
    print("samples =", 36)
    print("salt =", salt_hex)
    for i in range(36):
        token = int(input("tune = ").strip())
        token &= (1 << 64) - 1
        coeffs, pad, mask = derive(salt_hex, i, token, 10, 8, shift)
        mix = sum(c * b for c, b in zip(coeffs, B)) % q
        leak = ((mix + pad) % q) >> shift
        echo = leak ^ mask
        print("echo =", echo)

    print("submit sha256(','.join(map(str, B)))")
    ans = input("digest = ").strip().lower()
    if ans != digest:
        print("wrong")
        os._exit(0)

    print("nice :3")
    print(flag)

if __name__ == "__main__":
    signal.alarm(67)
    try:
        main()
    except Exception as e:
        print(e.__class__)