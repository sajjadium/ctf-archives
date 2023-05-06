from Crypto.Util.number import bytes_to_long, getPrime
from random import randint
from math import gcd
from secret import FLAG
from os import urandom


assert len(FLAG) < 100


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
    a = randint(0, p-1)

    return (p,a)


def main():
    p,a = generate_params()
    print("[+] The parameters of RNG:")
    print(f"{a=}")
    print(f"{p=}")
    b = int(input("[+] Inject [b]ackdoor!!: "))
    rng = lambda x: (x**2 + a*x + b) % p

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

    flag = bytes_to_long(FLAG + urandom(16))
    for n,e in keys:
        c = pow(flag, e, n)
        print("[+] Public Key:")
        print(f"{n=}")
        print(f"{e=}")
        print("[+] Cipher Text:", c)


if __name__ == "__main__":
    main()