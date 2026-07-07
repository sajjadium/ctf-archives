import os
import random

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import HKDF
from Crypto.Util.Padding import pad
from flask import Flask, jsonify


def _gf2_deg(p):
    return p.bit_length() - 1


def _gf2_divmod(a, b):
    db = _gf2_deg(b)
    r = a
    q = 0
    while r != 0 and _gf2_deg(r) >= db:
        shift = _gf2_deg(r) - db
        r ^= b << shift
        q ^= 1 << shift
    return q, r


def _gf2_mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result


def _gf2_xgcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    while r != 0:
        quot, rem = _gf2_divmod(old_r, r)
        old_r, r = r, rem
        old_s, s = s, old_s ^ _gf2_mul(quot, s)
    return old_r, old_s


def _poly_to_gf2_int(f):
    val = 0
    for i, c in enumerate(f):
        if c % 2 != 0:
            val |= 1 << i
    return val


def _gf2_int_to_poly(val, n):
    return [(val >> i) & 1 for i in range(n)]


def invert_mod2(f, n):
    modulus_poly = (1 << n) | 1
    a = _poly_to_gf2_int(f)
    gcd, x = _gf2_xgcd(a, modulus_poly)
    if gcd != 1:
        return None
    _, x = _gf2_divmod(x, modulus_poly)
    return _gf2_int_to_poly(x, n)


class NTRUParameters:
    def __init__(self, N=127, q=2048, p=3):
        self.N = N
        self.q = q
        self.p = p
        self.q_prime = 2053

    def poly_mult_mod(self, a, b, modulus):
        result = [0] * self.N
        for i in range(self.N):
            for j in range(self.N):
                idx = (i + j) % self.N
                result[idx] = (result[idx] + a[i] * b[j]) % modulus
        return result

    def poly_inverse_mod(self, f, modulus):
        return f

    def center_lift(self, a, modulus):
        return [(x - modulus) if x > modulus // 2 else x for x in a]


class NTRUChallenge:
    def __init__(self, params=None):
        self.params = params or NTRUParameters()
        self.f = None
        self.g = None
        self.h = None
        self.constraints = {}

    def generate_constrained_polynomial(
        self, target_sum_even, target_sum_odd, target_product_mod, seed=None
    ):
        if seed:
            random.seed(seed)

        N = self.params.N

        poly = [random.choice([-1, 0, 1]) for _ in range(N)]

        non_zero_count = sum(1 for x in poly if x != 0)
        while non_zero_count < (N + 1) // 2:
            idx = random.randint(0, N - 1)
            if poly[idx] == 0:
                poly[idx] = random.choice([-1, 1])
                non_zero_count += 1

        sum_even = sum(poly[i] for i in range(0, N, 2))
        sum_odd = sum(poly[i] for i in range(1, N, 2))

        return poly, {
            "sum_even": sum_even % 127,
            "sum_odd": sum_odd % 127,
            "product_sign": 1 if sum(poly) % 2 == 0 else -1,
        }

    def generate_keypair(self, seed=None):
        f_inv = None
        while f_inv is None:
            self.f, f_constraints = self.generate_constrained_polynomial(
                target_sum_even=42, target_sum_odd=37, target_product_mod=1, seed=seed
            )
            seed = None
            f_lifted = [(x % self.params.q) for x in self.f]
            f_inv = self.compute_inverse_simple(f_lifted, self.params.q)

        self.g, g_constraints = self.generate_constrained_polynomial(
            target_sum_even=31, target_sum_odd=29, target_product_mod=-1, seed=None
        )
        g_lifted = [(x % self.params.q) for x in self.g]

        self.constraints = {
            "f": f_constraints,
            "g": g_constraints,
            "modulus_constraint": 127,
            "N": self.params.N,
            "q": self.params.q,
        }

        self.h = self.params.poly_mult_mod(g_lifted, f_inv, self.params.q)

        return self.h

    def compute_inverse_simple(self, f, modulus):
        N = self.params.N

        f_inv = invert_mod2(f, N)
        if f_inv is None:
            return None

        for _ in range(6):
            prod = self.params.poly_mult_mod(f, f_inv, modulus)
            two_minus = [(-x) % modulus for x in prod]
            two_minus[0] = (2 - prod[0]) % modulus
            f_inv = self.params.poly_mult_mod(f_inv, two_minus, modulus)

        return f_inv

    def compute_algebraic_signature(self):
        fg_product = self.params.poly_mult_mod(self.f, self.g, self.params.q_prime)

        trace = sum(fg_product) % self.params.q_prime

        return trace

    def derive_encryption_key(self, salt):
        V = self.compute_algebraic_signature()

        ikm = (
            V.to_bytes(4, "big")
            + self.params.N.to_bytes(2, "big")
            + self.params.q.to_bytes(2, "big")
            + salt.encode("utf-8")
        )

        key = HKDF(
            master=ikm,
            key_len=32,
            salt=str(self.params.N).encode("utf-8"),
            hashmod=SHA256,
        )

        return key

    def encrypt_flag(self, flag, salt="lyknctf-2026"):
        key = self.derive_encryption_key(salt)

        cipher = AES.new(key, AES.MODE_CBC)
        ct = cipher.encrypt(pad(flag.encode("utf-8"), AES.block_size))

        return {"ciphertext": ct.hex(), "iv": cipher.iv.hex(), "salt": salt}

    def export_public_data(self, encrypted_flag):
        return {
            "parameters": {
                "N": self.params.N,
                "q": self.params.q,
                "p": self.params.p,
                "q_prime": self.params.q_prime,
                "ring": f"Z_{self.params.q}[x]/(x^{self.params.N} - 1)",
            },
            "public_key": {"h": self.h},
            "encrypted_flag": encrypted_flag,
        }

    def export_side_channel_leakage(self):
        return {
            "constraints": {
                "f_even_sum_mod_127": self.constraints["f"]["sum_even"],
                "f_odd_sum_mod_127": self.constraints["f"]["sum_odd"],
                "g_even_sum_mod_127": self.constraints["g"]["sum_even"],
                "g_odd_sum_mod_127": self.constraints["g"]["sum_odd"],
            },
            "constraint_modulus": 127,
        }


def generate_instance(flag):
    seed = int.from_bytes(os.urandom(4), "big")

    ntru = NTRUChallenge()
    print("[*] Generating ...")
    ntru.generate_keypair(seed=seed)

    print("[*] Encrypting flag...")
    encrypted = ntru.encrypt_flag(flag)

    public_data = ntru.export_public_data(encrypted)
    leakage = ntru.export_side_channel_leakage()

    print(
        f"[+] Instance generated (seed={seed}, "
        f"algebraic_signature={ntru.compute_algebraic_signature()})"
    )

    return public_data, leakage


FLAG = os.environ.get("FLAG", "LYKNCTF{test_flag_for_development_only}")
PUBLIC_DATA, SIDE_CHANNEL = generate_instance(FLAG)

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(
        {
            "challenge": "Whispering",
            "endpoints": {
                "/public.json": "lyknctf",
                "/side_channel.json": "lyknctf",
            },
        }
    )


@app.route("/public.json")
def public():
    return jsonify(PUBLIC_DATA)


@app.route("/side_channel.json")
def side_channel():
    return jsonify(SIDE_CHANNEL)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 9993)))
