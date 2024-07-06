#!/usr/bin/env python3
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from Crypto.Math.Numbers import Integer
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime, inverse, GCD
import json
import secrets
import os

FLAG = os.getenv("FLAG", "DUCTF{testflag}")

CURVE = "p256"

###
### Helpers
###


# ECDH helpers, from pycryptodome/Crypto/Protocol/DH.py
def _compute_ecdh(key_priv, key_pub):
    # See Section 5.7.1.2 in NIST SP 800-56Ar3
    pointP = key_pub.pointQ * key_priv.d
    if pointP.is_point_at_infinity():
        raise ValueError("Invalid ECDH point")
    return pointP.xy


def key_agreement(**kwargs):
    static_priv = kwargs.get("static_priv", None)
    static_pub = kwargs.get("static_pub", None)

    count_priv = 0
    count_pub = 0
    curve = None

    def check_curve(curve, key, name, private):
        if not isinstance(key, ECC.EccKey):
            raise TypeError("'%s' must be an ECC key" % name)
        if private and not key.has_private():
            raise TypeError("'%s' must be a private ECC key" % name)
        if curve is None:
            curve = key.curve
        elif curve != key.curve:
            raise TypeError("'%s' is defined on an incompatible curve" % name)
        return curve

    if static_priv is not None:
        curve = check_curve(curve, static_priv, "static_priv", True)
        count_priv += 1

    if static_pub is not None:
        curve = check_curve(curve, static_pub, "static_pub", False)
        count_pub += 1

    if (count_priv + count_pub) < 2 or count_priv == 0 or count_pub == 0:
        raise ValueError("Too few keys for the ECDH key agreement")

    return _compute_ecdh(static_priv, static_pub)


# Paillier encryption, from https://github.com/mikeivanov/paillier/
class Paillier_PublicKey:
    def __init__(self, n):
        self.n = n
        self.n_sq = n * n
        self.g = n + 1

    def encrypt(self, pt):
        while True:
            r = secrets.randbelow(self.n)
            if r > 0 and GCD(r, self.n) == 1:
                break
        x = pow(r, self.n, self.n_sq)
        ct = (pow(self.g, pt, self.n_sq) * x) % self.n_sq
        return ct


class Paillier_PrivateKey:
    def __init__(self, p, q, n):
        assert p * q == n
        self.l = (p - 1) * (q - 1)
        self.m = inverse(self.l, n)

    def decrypt(self, pub, ct):
        x = pow(ct, self.l, pub.n_sq) - 1
        pt = ((x // pub.n) * self.m) % pub.n
        return pt


def e_add(pub, a, b):
    """Add one encrypted integer to another"""
    return a * b % pub.n_sq


def e_add_const(pub, a, n):
    """Add constant n to an encrypted integer"""
    return a * pow(pub.g, n, pub.n_sq) % pub.n_sq


def e_mul_const(pub, a, n):
    """Multiplies an ancrypted integer by a constant"""
    return pow(a, n, pub.n_sq)


def generate_paillier_keypair(n_length):
    p = getPrime(n_length // 2)
    q = getPrime(n_length // 2)
    n = p * q
    return Paillier_PublicKey(n), Paillier_PrivateKey(p, q, n)


###
### Challenge
###


# Yehuda Lindell (2017). “Fast Secure Two-Party ECDSA Signing”
class Lindel17_Bob:
    def __init__(self):
        self.state = "gen_keys"
        self.exit = False

    def gen_keys(self, alice_ecdsa_pub):
        self.bob_ecdsa_priv = ECC.generate(curve=CURVE)

        # Calculate shared ecdsa public key
        shared_ecdsa_pub_x, shared_ecdsa_pub_y = key_agreement(static_pub=alice_ecdsa_pub, static_priv=self.bob_ecdsa_priv)
        self.shared_ecdsa_pub = ECC.construct(curve=CURVE, point_x=shared_ecdsa_pub_x, point_y=shared_ecdsa_pub_y)
        self.sig_scheme = DSS.new(self.shared_ecdsa_pub, "fips-186-3")

        # Bob encrypts his signing key and sends to Alice.
        self.paillier_pub, self.bob_paillier_priv = generate_paillier_keypair(n_length=2048)
        bob_ecdsa_priv_enc = self.paillier_pub.encrypt(int(self.bob_ecdsa_priv.d))

        return {
            "bob_ecdsa_pub": tuple(map(int, self.bob_ecdsa_priv.public_key().pointQ.xy)),
            "paillier_pub": {
                "g": self.paillier_pub.g,
                "n": self.paillier_pub.n,
            },
            "bob_ecdsa_priv_enc": bob_ecdsa_priv_enc,
        }

    def mul_share(self, alice_nonce_pub):
        self.bob_nonce_priv = ECC.generate(curve=CURVE)
        self.r, _ = key_agreement(static_pub=alice_nonce_pub, static_priv=self.bob_nonce_priv)

        return {"bob_nonce_pub": tuple(map(int, self.bob_nonce_priv.public_key().pointQ.xy))}

    def sign_and_validate(self, alice_partial_sig, message):
        alice_partial_sig = self.bob_paillier_priv.decrypt(self.paillier_pub, Integer(alice_partial_sig))

        k_b = self.bob_nonce_priv.d
        q = self.bob_nonce_priv._curve.order
        s = (k_b.inverse(q) * alice_partial_sig) % q

        signature = b"".join(long_to_bytes(x, self.sig_scheme._order_bytes) for x in (self.r, s))
        return signature, self.validate(message, signature)

    def validate(self, message, signature):
        try:
            self.sig_scheme.verify(SHA256.new(message), signature)
        except ValueError:
            return False
        return True

    def dispatch(self, request):
        if "action" not in request:
            return {"error": "please supply an action"}

        elif request["action"] == self.state == "gen_keys":
            self.state = "mul_share"

            x, y = request["x"], request["y"]
            alice_ecdsa_pub = ECC.construct(curve=CURVE, point_x=x, point_y=y)
            return self.gen_keys(alice_ecdsa_pub)

        elif request["action"] == self.state == "mul_share":
            self.state = "sign_and_validate"

            x, y = request["x"], request["y"]
            alice_nonce_pub = ECC.construct(curve=CURVE, point_x=x, point_y=y)
            return self.mul_share(alice_nonce_pub)

        elif request["action"] == self.state == "sign_and_validate":
            self.state = "mul_share"

            alice_partial_sig = request["partial_sig_ciphertext"]

            message = bytes.fromhex(request["message"])
            if message == b"We, Alice and Bob, jointly agree to declare war on the emus":
                return {"error": "What, no! I love emus??"}

            signature, is_valid = self.sign_and_validate(alice_partial_sig, message)
            if is_valid:
                return {"signature": signature.hex()}
            else:
                return {"error": "invalid signature parameters"}

        elif request["action"] == "get_flag":
            message = bytes.fromhex(request["message"])
            if message == b"We, Alice and Bob, jointly agree to declare war on the emus":
                signature = bytes.fromhex(request["signature"])
                if self.validate(message, signature):
                    return {"flag": FLAG}
            self.exit = True
            return {"error": "bad luck!"}
        else:
            return {"error": "unknown action"}


if __name__ == "__main__":
    print("Hi Alice, it's Bob! How're ya enjoying the party so far?")
    bob = Lindel17_Bob()

    for _ in range(1024):
        request = json.loads(input())
        response = bob.dispatch(request)
        print(json.dumps(response))
        if bob.exit:
            exit(0)
