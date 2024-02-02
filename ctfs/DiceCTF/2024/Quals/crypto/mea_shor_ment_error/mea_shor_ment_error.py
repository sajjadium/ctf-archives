import numpy as np
from Crypto.PublicKey import RSA

error_prob = 0.05

with open("privatekey.pem", "rb") as f:
    key = RSA.import_key(f.read())
p,q,n = key.p, key.q, key.n
mbits = 2 * key.size_in_bits()

euler = lcm(p-1, q-1)
P = prod(primes_first_n(10000))
factors = gcd(P^30, euler)
d = divisors(factors)
candidates = [(euler // x) for x in d]

rng = np.random.default_rng()

a = mod(1337, n)
r = min([x for x in candidates if a^x == 1])
assert gcd(n, mod(a,n)^(r//2) + 1) != 1

def sample_shor():
    
    j = randint(0, r-1)
    v = Integer((2^mbits * j)//r)

    res = v.digits(2)
    res = res + [0]*(mbits - len(res))
    res = res[::-1]

    error = rng.binomial(1, error_prob, mbits)
    res = [x^^y for x,y in zip(res, error)]
    res = "".join([str(i) for i in res])
    return res


data = "\n".join([str(sample_shor()) for i in range(1000)])
with open("shor.txt", "w") as f:
    f.write(data)