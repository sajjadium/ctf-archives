import json
import os
import hashlib
import random
from math import gcd, isqrt
from Crypto.Util.number import getPrime, inverse, GCD, bytes_to_long, long_to_bytes
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def lcm(a, b):
    return a * b // gcd(a, b)


def generate_vulnerable_rsa(bits=1536):
    print(f"[*] Generating {bits}-bit RSA parameters...")

    d_target_bits = int(bits * 0.205)

    attempts = 0
    while True:
        attempts += 1

        p = getPrime(bits // 2)
        q = getPrime(bits // 2)

        if p == q:
            continue

        N   = p * q
        phi = (p - 1) * (q - 1)
        g   = GCD(p - 1, q - 1)
        lambda_n = phi // g

        d = getPrime(d_target_bits)

        if GCD(d, phi) != 1:
            continue

        e = inverse(d, phi)

        wiener_bound = isqrt(isqrt(N)) // 3
        if d >= wiener_bound:
            continue

        assert (e * d - 1) % phi == 0,
        assert d < wiener_bound,

        print(f"[+] Found (attempt {attempts})")
        print(f"    N            = {N.bit_length()} bits")
        print(f"    d            = {d.bit_length()} bits  (target {d_target_bits} bits)")
        print(f"    e            = {e.bit_length()} bits")
        print(f"    N^0.25/3     = {wiener_bound.bit_length()} bits")
        print(f"    d ratio      = {d / wiener_bound:.6f}")

        return N, e, d, p, q, phi, lambda_n


def generate_leakages(p, q, phi, lambda_n):
    print("\n[*] Generating")
    M1 = 2**32 * 3 * 5 * 7 * 11
    M2 = 2**32 * 13 * 17 * 19
    R1 = (p - 1) % M1
    R2 = (q - 1) % M2

    leakage1 = {
        "R1": str(R1),
        "M1": str(M1),
        "R2": str(R2),
        "M2": str(M2),
    }
    print(f"[+] Leakage 1: p-1 ≡ {R1} (mod {M1})")
    print(f"               q-1 ≡ {R2} (mod {M2})")

    small_value = 2**20 * 3 * 5 * 7
    S = GCD(p + q, small_value)

    leakage2 = {
        "S": str(S),
        "small_value": str(small_value),
    }
    print(f"[+] Leakage 2: S = gcd(p+q, {small_value}) = {S}")

    M3 = 2**48 * 23 * 29 * 31
    lambda_mod = lambda_n % M3

    leakage3 = {
        "lambda_mod": str(lambda_mod),
        "modulus":    str(M3),
    }
    print(f"[+] Leakage 3: lambda ≡ {lambda_mod} (mod {M3})")

    return leakage1, leakage2, leakage3, S


def derive_aes_key(d, S, lambda_n, salt=b"FastLane-RSA-2024"):
    print("\n[*] Deriving...")

    d_bytes      = long_to_bytes(d)
    V_int        = d_bytes[:16]

    H1 = hashlib.sha256(V_int).digest()
    H2 = hashlib.sha256(long_to_bytes(S)).digest()
    H3 = hashlib.sha256(long_to_bytes(lambda_n)).digest()

    IKM = H1 + H2 + H3

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"FastLane-AES-Key"
    )
    aes_key = hkdf.derive(IKM)

    print(f"[+] V_int (hex): {V_int.hex()}")
    print(f"[+] H1    (hex): {H1.hex()[:32]}...")
    print(f"[+] H2    (hex): {H2.hex()[:32]}...")
    print(f"[+] H3    (hex): {H3.hex()[:32]}...")
    print(f"[+] Key   (hex): {aes_key.hex()}")

    return aes_key


def encrypt_flag(flag, aes_key):
    print("\n[*] Encrypting flag with AES-GCM...")

    aesgcm    = AESGCM(aes_key)
    nonce     = get_random_bytes(12)
    flag_bytes = flag.encode("utf-8")

    ciphertext = aesgcm.encrypt(nonce, flag_bytes, None)
    tag        = ciphertext[-16:]
    ct         = ciphertext[:-16]

    print(f"[+] Ciphertext : {ct.hex()[:64]}...")
    print(f"[+] Nonce      : {nonce.hex()}")
    print(f"[+] Tag        : {tag.hex()}")

    return ct, nonce, tag


def main():
    print("=" * 70)
    print("RSA Small-d Attack Parameter Generator")
    print("=" * 70)

    N, e, d, p, q, phi, lambda_n = generate_vulnerable_rsa(bits=1536)

    leakage1, leakage2, leakage3, S = generate_leakages(p, q, phi, lambda_n)
    aes_key = derive_aes_key(d, S, lambda_n)

    flag   = os.getenv("FLAG", "LYKNCTF{test_flag_for_fast_lane_rsa_boneh_durfee}")
    ct, nonce, tag = encrypt_flag(flag, aes_key)

    params = {
        "N":             str(N),
        "e":             str(e),
        "encrypted_flag": ct.hex(),
        "nonce":          nonce.hex(),
        "tag":            tag.hex(),
        "leakage1": leakage1,
        "leakage2": leakage2,
        "leakage3": leakage3,
    }

    with open("params.json", "w") as f:
        json.dump(params, f, indent=2)
    print("\n[+] Public parameters saved to params.json")

    private_data = {
        "p":       str(p),
        "q":       str(q),
        "d":       str(d),
        "phi":     str(phi),
        "lambda":  str(lambda_n),
        "S":       str(S),
        "aes_key": aes_key.hex(),
        "flag":    flag
    }

    with open("private.json", "w") as f:
        json.dump(private_data, f, indent=2)
    print("[+] Private data saved to private.json")

    print("\n" + "=" * 70)
    print("Generation complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
