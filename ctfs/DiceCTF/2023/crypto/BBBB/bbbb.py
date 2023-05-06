#!/usr/local/bin/python
from Crypto.Util.number import bytes_to_long, getPrime
from random import randint
from math import gcd
from os import urandom

def generate_key(rng, seed):
    e = rng(seed)
    while True:
        for _ in range(randint(10,100)):
            e = rng(e)
        p = getPrime(1024)
        q = getPrime(1024)
        phi = (p-1)*(q-1)
        if gcd(e, phi) == 1:
            break

    n = p*q
    return (n, e)


def generate_params():
    p = getPrime(1024)
    b = randint(0, p-1)

    return (p,b)


def main():
    p,b = generate_params()
    print("[+] The parameters of RNG:")
    print(f"{b=}")
    print(f"{p=}")
    a = int(input("[+] Inject b[a]ckdoor!!: "))
    rng = lambda x: (a*x + b) % p

    keys = []
    seeds = []
    for i in range(5):
        seed = int(input("[+] Please input seed: "))
        seed %= p
        if seed in seeds:
            print("[!] Same seeds are not allowed!!")
            exit()
        seeds.append(seed)
        n, e = generate_key(rng, seed)
        if e <= 10:
            print("[!] `e` is so small!!")
            exit()

        keys.append((n,e))

    FLAG = open("flag.txt", "rb").read()
    assert len(FLAG) < 50
    FLAG = FLAG + urandom(4)

    for n,e in keys:
        r = urandom(16)
        flag = bytes_to_long(FLAG + r)
        c = pow(flag, e, n)
        r = r.hex()
        print("[+] Public Key:")
        print(f"{n=}")
        print(f"{e=}")
        print(f"{r=}")
        print("[+] Cipher Text:", c)


if __name__ == "__main__":
    main()