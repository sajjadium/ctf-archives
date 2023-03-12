#!/usr/local/bin/python

from cryptography.hazmat.primitives.asymmetric import rsa
from secrets import randbits

if __name__ == '__main__':
    alice = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    print("Alice's pk: ", alice.public_key().public_numbers().n, alice.public_key().public_numbers().e)
    m = randbits(256)
    s = pow(m, alice.private_numbers().d, alice.public_key().public_numbers().n)
    print(m, s)
    print("Your key: ")
    n_prime = abs(int(input("n': ")))
    e_prime = abs(int(input("e': ")))
    d_prime = abs(int(input("d': ")))

    # Checks
    x = randbits(256)
    assert alice.public_key().public_numbers().n != n_prime or alice.public_key().public_numbers().e != e_prime
    assert n_prime > s
    assert pow(x, e_prime * d_prime, n_prime) == x
    assert e_prime > 1
    assert pow(s, e_prime, n_prime) == m

    with open('flag.txt', 'r') as f:
        print("Flag: " + f.read().strip())
