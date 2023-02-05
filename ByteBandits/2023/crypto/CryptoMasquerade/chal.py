import base64
import random
import math

from Crypto.Util import number
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

BIT_L = 2**8

with open("flag.txt", "r") as f:
    FLAG = f.read()


def generate_secrets():
    p = number.getPrime(BIT_L)
    g = number.getPrime(BIT_L)
    h = (p - 1) * (g - 1)
    a = 0
    while number.GCD(a, h) != 1:
        a = number.getRandomRange(3, h)
    b = pow(a, -1, h)
    return p * g, g, a, b


def main():
    p, g, a, b = generate_secrets()

    A = pow(g, a, p)
    B = pow(g, b, p)
    key = pow(A, b, p)

    print("p :", p)
    print("g :", g)
    print("A :", A)
    print("B :", B)
    print("key :", key)
    assert key == g

    password = key.to_bytes((key.bit_length() + 7) // 8, "big")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=b"\x00" * 8,
        iterations=100000,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    token = f.encrypt(FLAG.encode("ascii"))

    print("message : ", token.decode())


if __name__ == "__main__":
    main()
