from Crypto.Util.number import getPrime, isPrime, bytes_to_long


def sus(sz, d):
    while True:
        p = getPrime(sz)
        pp = sum([p**i for i in range(d)])
        if isPrime(pp):
            return p, pp


p, q = sus(512, 3)
r = getPrime(512 * 3)
n = p * q * r
e = 65537
m = bytes_to_long(open("flag.txt", "rb").read().strip())
c = pow(m, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{c = }")
