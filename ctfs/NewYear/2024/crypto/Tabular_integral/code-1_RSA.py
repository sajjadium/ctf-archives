from Crypto.Util.number import getPrime , bytes_to_long , GCD
import random

random.seed()
flag = b'grodno{fake_flag}'

KEY_SIZE = 512
RSA_E = 65535

def gen_RSA_params(N, e):
    while True:
        p, q = getPrime(N), getPrime(N)
        if GCD(e, (p - 1) * (q - 1)) == 1: break
    n = p * q
    check(p, q, n) 
    return (p, q, n)

def check(p, q, n):
    a_ = random.randint(1, 100000)
    b_ = random.randint(1, 100000)
    c_ = random.randint(1, 100000)
    d_ = random.randint(1, 100000)
    s = pow_m(p, pow_m(q, a_, c_ * (p - 1) * (q - 1)), n)
    t = pow_m(q, pow_m(p, b_, d_ * (p - 1) * (q - 1)), n)
    result = s + t
    print(f"result = {result}")

def pow_m(base, degree, module):
    degree = bin(degree)[2:]
    r = 1
    for i in range(len(degree) - 1, -1, -1):
        r = (r * base ** int(degree[i])) % module
        base = (base ** 2) % module
    return r

dp, q, n = gen_RSA_params(KEY_SIZE, RSA_E) 

m = bytes_to_long(flag)
c = pow(m, RSA_E, n)

print(f"e = {RSA_E}")
print(f"n = {n}")
print(f"c = {c}")
