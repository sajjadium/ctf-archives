import hashlib
import random
import ast
from math import log
from flag import flag

"""
This implements Winternitz one-time signatures as defined in http://toc.cryptobook.us
"""

# Define Winternitz parameters

v = 256  # maximum bits for message size
hash_size = 32
d = 15  # base

n_0 = 64
assert (d + 1) ** n_0 == 2**v

n_1 = int(log(n_0, d + 1)) + 1
n = n_0 + n_1


def get_hash(x: bytes) -> bytes:
    return hashlib.sha256(x).digest()


def hash_chain(x: bytes, d: int) -> bytes:
    for _ in range(d):
        x = get_hash(x)
    return x


def int_to_vec(m: int, vec_len: int, base: int) -> list[int]:
    # Given an integer, output a vector that represents the digits of m in the
    # specified base (big-endian)
    digits = [0] * vec_len
    i = len(digits) - 1
    while m > 0:
        digits[i] = m % base
        m //= base
        i -= 1
    return digits


def domination_free_function(m: int) -> list[int]:
    # This function maps an integer to a vector.
    # What is a domination free function?
    # Let f(a) = xs
    # Let f(b) = ys
    # If f is a domination free function, then
    # all(x[i] >= y[i] for i in range(len(xs)))
    # must be false for any integers a and b.

    m_vec = int_to_vec(m, n_0, d + 1)

    # Compute checksum
    c = (d * n_0) - sum(m_vec)
    c_vec = int_to_vec(c, n_1, d + 1)

    return m_vec + c_vec


class Winternitz:
    def __init__(self):
        # Secret key stuff
        self.secret = random.SystemRandom().getrandbits(v)
        prg = random.Random(self.secret)
        self.xs = [prg.randbytes(hash_size) for _ in range(n)]

        # Public key stuff
        self.ys = [hash_chain(x, d) for x in self.xs]

    def public_key(self) -> bytes:
        return get_hash(b"".join(self.ys))

    def sign(self, m: bytes) -> list[bytes]:
        if len(m) * 8 > v:
            raise ValueError("Message too long")

        ss = domination_free_function(int.from_bytes(m, "big"))
        return [hash_chain(self.xs[i], s) for i, s in enumerate(ss)]

    def verify(self, public_key: bytes, m: bytes, signature: list[bytes]):
        ss = domination_free_function(int.from_bytes(m, "big"))
        ys = [hash_chain(signature[i], d - s) for i, s in enumerate(ss)]
        return public_key == get_hash(b"".join(ys))


def main():
    print("Welcome to my signing service!")

    w = Winternitz()
    pk = w.public_key()
    print(f"Public key: {pk.hex()}")

    print("Enter a message to sign as hex string:")
    m = bytes.fromhex(input(">>> "))
    if b"admin" in m:
        print("Not authorized")
        return

    sig = w.sign(m)
    print(f"Your signature is:")
    print(sig)

    print()
    print("Can you forge a signature for another message?")

    print("Enter a new message to sign as a hex string:")
    m_new = bytes.fromhex(input(">>> "))
    if m == m_new:
        print("Repeated message")
        return

    print("Enter signature:")
    forged_sig = ast.literal_eval(input(">>> "))
    print(forged_sig)
    if type(forged_sig) is not list:
        print("Bad signature")
        return
    if len(forged_sig) != n:
        print("Bad signature")
        return
    if not all(type(x) is bytes for x in forged_sig):
        print("Bad signature")
        return
    if not all(len(x) == hash_size for x in forged_sig):
        print("Bad signature")
        return

    if w.verify(pk, m_new, forged_sig):
        if b"admin" in m_new:
            print("You must be the admin, so here's your flag:")
            print(flag)
        else:
            print("Valid signature, but you're not admin")
    else:
        print("Signature failed to verify")


if __name__ == "__main__":
    main()
