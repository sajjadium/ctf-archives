import os
import random
import string

MODULUS = 100000000000000000000000000000000000000000000000151
PRIVATE_KEY_1 = "LITCTF{[redacted]}"
assert len(PRIVATE_KEY_1) < MODULUS.bit_length() // 8
PRIVATE_KEY_2 = os.urandom(32)

def r(n):
    b = bin(n)[2:]
    o = [i for i, c in enumerate(b) if c == '1']
    m = sum(1 << (len(b) - 1 - i) for i in o)
    return n ^ m


def t(n):
    cnt = 0
    while n < MODULUS/2 and cnt < 100:
        cnt += 1
        n *= 2
        n %= MODULUS
    return n

def s(user_input_str):
    combined = PRIVATE_KEY_1 + user_input_str
    combined_bytes = combined.encode()
    combined_int = int.from_bytes(combined_bytes, byteorder='big')
    rng = random.Random(PRIVATE_KEY_2)
    res = combined_int
    for i in range(1000):
        randnum = rng.randint(10**49, 10**50)
        res = (res * t(randnum) + r(randnum)) % MODULUS
    return res

for i in range(2):
    strlen = random.randint(100, 1000)
    inpstr = ""
    for j in range(strlen):
        inpstr += random.choice(string.ascii_letters + string.digits)
    print("input string: ", inpstr)
    output = s(inpstr)
    print(f"Final result: {output}")