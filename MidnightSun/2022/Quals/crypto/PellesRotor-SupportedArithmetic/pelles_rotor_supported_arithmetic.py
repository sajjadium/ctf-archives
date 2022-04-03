#!/usr/bin/python3
from sys import stdin, stdout, exit
from flag import FLAG
from secrets import randbelow
from gmpy import next_prime

p = int(next_prime(randbelow(2**512)))
q = int(next_prime(randbelow(2**512)))
n = p * q
e = 65537

phi = (p - 1)*(q - 1)
d = int(pow(e, -1, phi))
d_len = len(str(d))

print("encrypted flag", pow(FLAG, 3331646268016923629, n))
stdout.flush()

ctr = 0
def oracle(c, i):
    global ctr
    if ctr > 10 * d_len // 9:
        print("Come on, that was already way too generous...")
        return
    ctr += 1
    rotor = lambda d, i: int(str(d)[i % d_len:] + str(d)[:i % d_len])
    return int(pow(c, rotor(d, i), n))

banner = lambda: stdout.write("""
Pelle's Rotor Supported Arithmetic Oracle
1) Query the oracle with a ciphertext and rotation value.
2) Exit.
""")

banner()
stdout.flush()

choices = {
    1: oracle,
    2: exit
}

while True:
    try:
        choice = stdin.readline()
        print("c:")
        stdout.flush()
        cipher = stdin.readline()
        print("rot:")
        stdout.flush()
        rotation = stdin.readline()
        print(choices.get(int(choice))(int(cipher), int(rotation)))
        stdout.flush()
    except Exception as e:
        stdout.write("%s\n" % e)
        stdout.flush()
        exit()

