import os
import random
from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long
from sympy.polys.matrices import DomainMatrix
from sympy import FiniteField

# secret import
from secret import decrypt
from flag import FLAG


size = 1024//8
e = 65537


def pad(data, length):
    if len(data) >= length:
        raise ValueError("length of data is too large.")
    pad_data = bytes([random.randint(1, 255) for _ in range(length - len(data) - 1)])
    return pad_data + b'\x00' + data


def unpad(paddeddata):
    if b'\x00' not in paddeddata:
        raise ValueError("padding is incorrect.")
    return paddeddata[paddeddata.index(b'\x00')+1:]


def keygen():
    p, q = getPrime(8*size), getPrime(8*size)
    n = p*q
    return ((p, q), n)


def encrypt(msgint, n):
    a = bytes_to_long(os.urandom(int(2*size-1)))
    # sympy.FiniteField treats non-prime modulus instance as Z/nZ
    Zmodn = FiniteField(n)
    mat = DomainMatrix([
            [Zmodn(a), Zmodn(msgint)],
            [Zmodn(0), Zmodn(a)]
        ], (2, 2), Zmodn)

    enc = mat**int(e)
    enc_0 = int(enc[0,0].element.val)
    enc_1 = int(enc[0,1].element.val)
    return (enc_0, enc_1)


def main():
    try:
        banner = "Welcome to matrix RSA world"
        print(banner)

        (p,q), n = keygen()

        paddedflag = pad(FLAG, 2*size-1)
        assert unpad(paddedflag) == FLAG
        paddedflagint = bytes_to_long(paddedflag)
        encflag_0, encflag_1 = encrypt(paddedflagint, n)
        assert decrypt((encflag_0, encflag_1), (p, q)) == paddedflagint
        print("Here is encrypted flag(enc_0, enc_1):")
        print(long_to_bytes(encflag_0).hex())
        print(long_to_bytes(encflag_1).hex())

        while True:
            print("Please input encrypted message(enc_0, enc_1):")
            enc_0 = bytes_to_long(bytes.fromhex(input('>> ')))
            enc_1 = bytes_to_long(bytes.fromhex(input('>> ')))
            if enc_0 >= n or enc_1 >= n:
                print("size error")
                continue
            if (enc_0 * encflag_1 - enc_1 * encflag_0) % n == 0:
                print("Do not input related to encrypted flag")
                continue
            dec = decrypt((enc_0, enc_1), (p, q))
            if FLAG in long_to_bytes(dec):
                print("Do not input encrypted flag")
            else:
                print("Here is decrypted message:")
                print(long_to_bytes(int(dec)).hex())
    except:
        quit()


if __name__ == "__main__":
    main()
