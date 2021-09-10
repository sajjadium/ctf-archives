from string import ascii_uppercase, ascii_lowercase, digits
from random import randrange, choice
from Crypto.PublicKey import DSA
from hashlib import sha1
from gmpy2 import xmpz, to_binary, invert, powmod, is_prime


def gen_rand_str(size=40, chars=ascii_uppercase + ascii_lowercase + digits):
    return ''.join(choice(chars) for _ in range(size))


def gen_g(p, q):
    while True:
        h = randrange(2, p - 1)
        exp = xmpz((p - 1) // q)
        g = powmod(h, exp, p)
        if g > 1:
            break
    return g


def keys(g, p, q):
    d = randrange(2, q)
    e = powmod(g, d, p)
    return e, d


def sign(msg, k, p, q, g, d):
    while True:
        r = powmod(g, k, p) % q
        h = int(sha1(msg).hexdigest(), 16)
        try:
            s = (invert(k, q) * (h + d * r)) % q
            return r, s
        except ZeroDivisionError:
            pass


if __name__ == "__main__":
    print("\n")
    print(".___________..___  ___.  __    __    ______ .___________. _______     ___     ___    ___    __  ")
    print("|           ||   \/   | |  |  |  |  /      ||           ||   ____|   |__ \   / _ \  |__ \  /_ | ")
    print('`---|  |----`|  \  /  | |  |  |  | |  ,----"`---|  |----`|  |__         ) | | | | |    ) |  | | ')
    print("    |  |     |  |\/|  | |  |  |  | |  |         |  |     |   __|       / /  | | | |   / /   | | ")
    print("    |  |     |  |  |  | |  `--'  | |  `----.    |  |     |  |         / /_  | |_| |  / /_   | | ")
    print("    |__|     |__|  |__|  \______/   \______|    |__|     |__|        |____|  \___/  |____|  |_| ")

    steps = 10
    for i in range(steps):
        key = DSA.generate(2048)
        p, q = key.p, key.q
        print("\n\nq =", q)
        g = gen_g(p, q)
        e, d = keys(g, p, q)
        k = randrange(2, q)
        msg1 = gen_rand_str()
        msg2 = gen_rand_str()
        msg1 = str.encode(msg1, "ascii")
        msg2 = str.encode(msg2, "ascii")
        r1, s1 = sign(msg1, k, p, q, g, d)
        r2, s2 = sign(msg2, k, p, q, g, d)
        print("\nsign('" + msg1.decode() + "') =", s1)
        print("\nsign('" + msg2.decode() + "') =", s2)
        if i == (steps - 1):
            with open('flag', 'rb') as f:
                flag = f.read()
                secret = flag
        else:
            secret = gen_rand_str()
            secret = str.encode(secret, "ascii")
        r3, s3 = sign(secret, k, p, q, g, d)
        print("\nsign(secret) =", s3, r3)
        h = input("\nGive me SHA1(secret) : ")
        if h == str(int(sha1(secret).hexdigest(), 16)):
            print("\nThat's right, the secret is", secret.decode())
        else:
            print("\nSorry, I cannot give you the secret. Bye!")
            break
