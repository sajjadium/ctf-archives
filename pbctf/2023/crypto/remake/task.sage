import os 

flag = open("flag", "rb").read()
flag = flag.lstrip(b"pbctf{").rstrip(b"}")
assert len(flag) == 192

while True:
    p = random_prime(1 << 513, lbound = 1 << 512)
    coefs = [int.from_bytes(os.urandom(42), "big") for _ in range(8)]
    PR.<x> = PolynomialRing(GF(p))

    g1, g2 = 2, 3
    f1 = sum(coefs[i] * (x ** i) for i in range(2 * g1 + 2))
    f2 = sum(coefs[i] * (x ** i) for i in range(2 * g2 + 2))

    flag1 = GF(p)(int.from_bytes(flag[:64], "big"))
    flag2 = GF(p)(int.from_bytes(flag[64:128], "big"))
    flag3 = GF(p)(int.from_bytes(flag[128:], "big"))
    hint = GF(p)(int.from_bytes(b"Inspired by theoremoon's SECCON 2022 Finals Challenge - Hell. Thank you!", "big"))

    pol1 = x * x - f1(flag1)
    pol2 = x * x - f1(flag2)
    pol3 = x * x - f2(flag3)
    pol4 = x * x - f2(hint)

    if len(pol1.roots()) * len(pol2.roots()) * len(pol3.roots()) * len(pol4.roots()) == 0:
        continue 

    HC1 = HyperellipticCurve(f1, 0)
    J1 = HC1.jacobian()(GF(p))

    HC2 = HyperellipticCurve(f2, 0)
    J2 = HC2.jacobian()(GF(p))

    P1 = HC1((flag1, pol1.roots()[0][0]))
    P2 = HC1((flag2, pol2.roots()[0][0]))
    P3 = HC2((flag3, pol3.roots()[0][0]))
    P4 = HC2((hint, pol4.roots()[0][0]))

    print(2 * J1(P1) + 2 * J1(P2))
    print(5 * J2(P3))
    print(J2(P4))
    break