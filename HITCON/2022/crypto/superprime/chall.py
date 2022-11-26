from Crypto.Util.number import getPrime, isPrime, bytes_to_long


def getSuperPrime(nbits):
    while True:
        p = getPrime(nbits)
        pp = bytes_to_long(str(p).encode())
        if isPrime(pp):
            return p, pp


p1, q1 = getSuperPrime(512)
p2, q2 = getSuperPrime(512)
p3, q3 = getSuperPrime(512)
p4, q4 = getSuperPrime(512)
p5, q5 = getSuperPrime(512)

n1 = p1 * q1
n2 = p2 * p3
n3 = q2 * q3
n4 = p4 * q5
n5 = p5 * q4

e = 65537
c = bytes_to_long(open("flag.txt", "rb").read().strip())
for n in sorted([n1, n2, n3, n4, n5]):
    c = pow(c, e, n)

print(f"{n1 = }")
print(f"{n2 = }")
print(f"{n3 = }")
print(f"{n4 = }")
print(f"{n5 = }")
print(f"{e = }")
print(f"{c = }")
