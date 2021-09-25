#!/usr/bin/env sage

proof.arithmetic(False) # just makes things faster

def get_3m4_prime(N):
    while True:
        p = random_prime(2^N - 1, lbound=2^(N-1))
        if p % 4 == 3:
            return p

def generate_key(L, n, m):
    p = get_3m4_prime(L//2)
    q = get_3m4_prime(L//2)
    N = p*q
    r = next_prime(N)
    F.<x> = PolynomialRing(GF(r))
    K = F.quo(F.irreducible_element(n))
    return (K, m), N, (p, q)

def H(params, msg, u):
    K, m = params
    r, z = K.characteristic(), K.gens()[0]
    h = 0
    while msg > 0:
        h *= z
        h += msg % r
        msg //= r
    h += z*u
    for _ in range(m):
        h ^= r
    assert len(list(h)) != 0
    return int(h[0])

def sign(params, privkey, msg):
    p, q = privkey
    u = 1
    while True:
        c = H(params, msg, u) % (p*q)
        if legendre_symbol(c, p) == legendre_symbol(c, q) == 1:
            break
        u += 1
    xp = pow(c, (p+1)//4, p)
    xq = pow(c, (q+1)//4, q)
    x = crt([int(xp), int(xq)], [p, q])
    return x, u

def verify(params, pubkey, msg, sig):
    N = pubkey
    x, u = sig
    c = H(params, msg, u)
    return x^2 % N == c % N

def main():
    print('Welcome to the game. To get the flag, give me a message to sign, then sign a random message of mine!')
    FLAG = open('./flag.txt', 'r').read().strip()

    L, n, m = 1024, 15, 3
    params, pubkey, privkey = generate_key(L, n, m)
    print('N:', pubkey)

    msg = int(input('message (in hex): '), 16)
    if msg < pubkey^m:
        print('That message is too small!')
        exit()
    if msg > pubkey^n:
        print('That message is too big!')
        exit()
    x, u = sign(params, privkey, msg)
    print('x:', x)
    print('u:', u)

    auth_msg = randint(1, pubkey^5)
    print('Now sign', hex(auth_msg))
    x = int(input('x: '))
    u = int(input('u: '))

    if verify(params, pubkey, auth_msg, (x, u)):
        print(FLAG)
    else:
        print('Incorrect!')

if __name__ == '__main__':
    main()
