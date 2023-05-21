import sys

import random
from Crypto.PublicKey import RSA

import secret

difficulty = 128
degree = 8


def generate_rsa_key():
    while True:
        key = RSA.generate(1024)
        e = 47
        n, p, q = key.n, key.p, key.q
        if secret.is_hard_enough(e, p, q, difficulty):
            return e, key.p, key.q
        else: # just so you know it's not some super unusual key
            print("Key retry")


def printout(msg):
    sys.stdout.write(str(msg) + "\n")
    sys.stdout.flush()


def polynomial_value(x, coefficients):
    return sum([coefficients[i] * x ** i for i in range(degree + 1)])


def validate(coefficients, values, e, n):
    random.shuffle(values)
    return all([polynomial_value(pow(v, e, n), coefficients) == v for v in values])


def read_coefficients():
    return [int(input("coefficient for x^{} ".format(i))) for i in range(degree + 1)]


def main():
    try:
        e, p, q = generate_rsa_key()
        printout("You have a chance to prove that you've completely broken RSA!")
        printout("Give me a polynomial of degree {} which can act as RSA decryption oracle.".format(degree))
        coefficients = read_coefficients()
        printout("Just so you can verify I'm not cheating, the key (e,p,q) is:")
        printout(e)
        printout(p)
        printout(q)
        printout(
            "Please provide {} distinct plaintext numbers (comma separated), which your function is able to decrypt, based on their encrypted version".format(
                difficulty))
        values = [int(x) for x in input().split(",")]
        assert len(values) == difficulty
        assert len(set(values)) == difficulty
        assert all([0 <= v < p * q for v in values])
        if validate(coefficients, values, e, p * q):
            printout(open("flag.txt", "rb").read())
    except:
        printout("Nope :(")


main()
