from Crypto.Util.number import bytes_to_long
from random import randrange
from secret import FLAG
from signal import alarm

def miller_rabin(bases, n):
    if n == 2 or n == 3:
        return True

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    
    for b in bases:
        x = pow(b, s, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n-1:
                break
        else:
            return False
    return True

def is_prime(n):
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 31337]
    for i in range(2,min(256, n)):
        if n%i == 0:
            return False
    if n < 256:
        return True
    return miller_rabin(bases, n)

LLIM = 2**512
ULIM = 2**1024

def die(msg):
    print("[X] " + msg)
    quit()

def verify_n_is_safe_prime(factors):
    N = 1
    for p in factors:
        N *= p
        if not is_prime(p):
            die("This factor is not prime!")
    N += 1

    if max(factors) < LLIM:
        die("Smooth N is not safe.")
    if not is_prime(N):
        die("This N is not prime!")
    if LLIM > N or N > ULIM:
        die("This N is out of range.")
    return N


def main():
    msg = bytes_to_long(FLAG)
    token = randrange(ULIM)
    msg ^= token
    print(f"[$] Here's your token for the session: {token}")
    alarm(60)

    blacklist = []
    for _ in range(5):
        user_input = input("[?] Give me the prime factors of phi(N): ").strip().split(' ')
        phi_factors = [int(x) for x in user_input]
        N = verify_n_is_safe_prime(phi_factors)
        if N in blacklist:
            die("No reusing N allowed!")
        x = randrange(N)
        print(f"[$] {x = }")
        out = pow(x, msg, N)
        print(f"[$] {out = }")
        blacklist.append(N)


if __name__ == '__main__':
    main()
