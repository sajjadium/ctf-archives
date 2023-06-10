import random
import time
from Crypto.Util.number import bytes_to_long, isPrime

from secret import FLAG


def fail():
    print("You have disappointed the pigeon.")
    exit(-1)


def generate_prime_number(bits: int = 128) -> int:
    num = random.getrandbits(bits)
    while not isPrime(num):
        num += 1
    return num


def generate_random_boolean() -> bool:
    return bool(random.getrandbits(1))


def first_verify(g, p, y, C, w, r) -> bool:
    assert w
    return ((y * C) % p) == pow(g, w, p)


def second_verify(g, p, y, C, w, r) -> bool:
    assert r
    return pow(g, r, p) == C


p = generate_prime_number()
g = random.getrandbits(128)
x = bytes_to_long(FLAG.encode())
y = pow(g, x, p)

print(f"p = {p}")
print(f"g = {g}")
print(f"y = {y}")

print("Something something zero-knowledge proofs blah blah...")
print("Why not just issue the challenge and the verification at the same time? Saves TCP overhead!")

seen_c = set()
for round in range(30):
    w, r = None, None
    choice = generate_random_boolean()
    if not choice:
        w = int(input("Enter w: "))
        C = int(input("Enter C: "))
        if C in seen_c:
            fail()
        seen_c.add(C)
        verify = first_verify
    else:
        r = int(input("Enter r: "))
        C = int(input("Enter C: "))
        if C in seen_c:
            fail()
        seen_c.add(C)
        verify = second_verify
    if not verify(g, p, y, C, w, r):
        fail()
    else:
        print(f"You passed round {round + 1}.")
time.sleep(1)
print(
    "You were more likely to get hit by lightning than proof correctly 30 times in a row, you must know the secret right?"
)
print(f"A flag for your troubles - {FLAG}")
