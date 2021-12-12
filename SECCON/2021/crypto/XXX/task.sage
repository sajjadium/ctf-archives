import os

flag = os.getenv("FLAG", "fake{fakeflag_blahblah}")
x = int.from_bytes(flag.encode(), "big")

p = random_prime(1 << int(x.bit_length() * 2.5))
Fp = GF(p)

params = []
while len(params) != 6:
    try:
        y = randint(2, x)
        a = randint(2, p-1)
        b = (y^2 - (x^3 + a*x)) % p

        EC = EllipticCurve(Fp, [a, b])
        EC(x, y)

        params.append([a, b])
    except ValueError:
        pass

print(p)
print(params)
