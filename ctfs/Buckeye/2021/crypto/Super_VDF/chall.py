from gmpy2 import is_prime, mpz
from random import SystemRandom

rand = SystemRandom()
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]


def get_prime(bit_length):
    while True:
        x = mpz(1)
        while x.bit_length() < bit_length:
            x *= rand.choice(PRIMES)
        if is_prime(x + 1):
            return x + 1


def get_correct_answer():
    # Implementation redacted
    return -1


p = get_prime(1024)
q = get_prime(1024)
n = p * q

print(f"n = {n}")
print("Please calculate (59 ** 59 ** 59 ** 59 ** 1333337) % n")
ans = int(input(">>> "))

if ans == get_correct_answer():
    print("WTF do you own a supercomputer? Here's your flag:")
    print("buckeye{????????????????????????????????????}")
else:
    print("WRONG")
