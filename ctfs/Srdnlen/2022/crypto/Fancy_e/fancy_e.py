#!/usr/bin/env python3

import random
import string

from Crypto.Util.number import getPrime, bytes_to_long


def flag_padding(flag):
    s = string.ascii_lowercase + string.ascii_uppercase + string.digits
    for i in range(random.randint(5, 10)):
        flag = random.choice(s) + flag + random.choice(s)
    return flag


def fancy_e(b, x, y):
    rand1 = random.randint(1, 5)
    rand2 = random.randint(1, 5)
    rand3 = random.randint(1, 5)

    op1 = random.choice([-1, 1])
    op2 = random.choice([-1, 1])
    op3 = random.choice([-1, 1])

    e = b + (op1 * rand1)
    f = x * y + op2 * rand2 * y + op3 * rand3 * x + 1
    k = rand1 + rand2 + rand3

    new_e = (e * f * k + 1) | 1

    assert pow(new_e, -1, (x - 1) * (y - 1))

    return new_e


flag = open('flag.txt', 'r').read()
flag = flag_padding(flag)
base = int(open('base.txt', 'r').read())
assert 300 < base < 1000

disclaimer = "Tired of using e = 65537? Would you prefer a more stylish and original e to encrypt your message?\n" \
             "Try my new software then! It is free, secure and sooooo cool\n" \
             "Everybody will envy your fancy e\n" \
             "You can have a look to up to 1000 flags encrypted with my beautiful e and " \
             "choose the one you like the most\n" \
             "How many do you want to see?"

print(disclaimer)
number = int(input("> "))
if number < 1 or number > 1000:
    print("I said up to 1000! Pay for more")
    exit(1)
print()

i = 0
while i < number:
    p = getPrime(256)
    q = getPrime(256)
    n = p * q
    try:
        e = fancy_e(base, p, q)
        ct = pow(bytes_to_long(flag.encode()), e, n)
        print("Ciphertext"+str(i)+"= " + str(ct))
        print("e"+str(i)+"=          " + str(e))
        print("Modulus"+str(i)+"=    " + str(n))
        print()
        i += 1

    except:
        continue
