import random
from sympy import nextprime, mod_inverse


def gen_primes(bit_length, diff=2**32):
    p = nextprime(random.getrandbits(bit_length))
    q = nextprime(p + random.randint(diff//2, diff))
    return p, q


def gen_keys(bit_length=1024):
    p, q = gen_primes(bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    d = mod_inverse(e, phi)

    return (n, e)


def encrypt(message, public_key):
    n, e = public_key
    message_int = int.from_bytes(message.encode(), 'big')
    ciphertext = pow(message_int, e, n)
    return ciphertext


if __name__ == "__main__":
    public_key = gen_keys()

    message = "FLAG"
    ciphertext = encrypt(message, public_key)

    f = open("easy_rsa.txt", "a")
    f.write(f"n: {public_key[0]} \n")
    f.write(f"e: {public_key[1]} \n")
    f.write(f"c: {ciphertext}")
    f.close()
