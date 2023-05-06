from Crypto.Util.number import bytes_to_long, getPrime, getRandomInteger, isPrime
from secret import flag


def create_prime(p_bit_len, add_bit_len, a):
    p = getPrime(p_bit_len)
    p_bit_len2 = 2*p_bit_len // 3 + add_bit_len
    while True:
        b = getRandomInteger(p_bit_len2)
        _p = a * p
        q = _p**2 + 3*_p*b + 3*b**2
        if isPrime(q):
            return p, q


def encrypt(p_bit_len, add_bit_len, a, plain_text):
    p, q = create_prime(p_bit_len, add_bit_len, a)
    n = p*q
    e = 65537

    c = pow(plain_text, e, n)
    print(f"{n=}")
    print(f"{e=}")
    print(f"{c=}")
    print(f"{a=}")


if __name__ == "__main__":
    encrypt(1024, 9, 23, bytes_to_long(flag))