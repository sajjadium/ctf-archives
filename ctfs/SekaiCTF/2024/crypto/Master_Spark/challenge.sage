from Crypto.Util.number import *
import os
from timeout_decorator import timeout, TimeoutError

load("GA.sage")

FLAG = os.getenv("FLAG")
secret = getPrime(256)
choice = set()


@timeout(60)
def T_T(p, primes, secret):

    assert isPrime(p)
    assert len(primes) > 3

    Fp = GF(p)
    Fp2.<j> =  GF(p ^ 2, modulus=x ^ 2 + 1)
    ls = len(factor(p + 1)) - 2

    m = ceil((sqrt(p) ** (1 / ls) - 1) / 2)
    alice_priv = [randrange(-m, m + 1) for _ in range(len(primes))]
    bob_priv = [randrange(-m, m + 1) for _ in range(len(primes))]
    EC = montgomery(Fp2, 0)
    P = EC.gens()[0]
    k = 1
    alice_pub, Q = group_action(p, primes, Fp, Fp2, 0, alice_priv, k * P)
    share_bob, Q = group_action(p, primes, Fp, Fp2, alice_pub, bob_priv, secret * Q)
    bob_pub, P = group_action(p, primes, Fp, Fp2, 0, bob_priv, P)
    share_alice, P = group_action(p, primes, Fp, Fp2, bob_pub, alice_priv, P)
    return P, Q


def check(p):
    assert isPrime(p)
    assert p.bit_length() <= 96
    assert ((p + 1) // 4) % 2 == 1
    prime_list = []
    cnt = 0

    for p, i in factor((p + 1) // 4):
        assert not p in choice
        if i > 1:
            cnt += 1
            choice.add(p)
            assert int(p).bit_length() <= 32
        else:
            prime_list.append(p)
            choice.add(p)

    assert all([int(p).bit_length() <= 16 for p in prime_list])
    assert cnt == 1

    return prime_list


def main():
    while True:
        try:
            p = int(input("input your prime number or secret > "))
            if int(p).bit_length() == 256:
                if p == secret:
                    print(FLAG)
                    exit()
                print("not flag T_T")
            else:
                prime_list = check(p)
                P, Q = T_T(p, prime_list, secret)
                print(P.xy())
                print(Q.xy())
        except:
            print("T_T")
            exit()
main()
