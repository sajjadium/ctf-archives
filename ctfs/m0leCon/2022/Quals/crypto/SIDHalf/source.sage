with open("flag.txt") as f:
    flag = f.read().strip()

flag = flag.encode()

# Setup SIDH params
lA,eA, lB,eB = 2,91, 3,57
p = lA^eA * lB^eB - 1
F.<i> = GF(p^2, modulus=x^2+1)
E0 = EllipticCurve(F, [1,0])
PA, QA = (lB^eB * G for G in E0.gens())
PB, QB = (lA^eA * G for G in E0.gens())
print(PA, QA, PB, QB)

# Some new isogeny encoding
def encode_byte(val):
    privB = randrange(lB^eB)
    KB = PB + privB*QB
    phiB = E0.isogeny(KB, algorithm="factored")
    EB = phiB.codomain()
    GB, HB = phiB(PA), phiB(QA)

    U = lB^eB * EB.random_element()
    V = lB^eB * EB.random_element()

    G = GB-val*U
    H = HB-val*V

    return ((EB.a4(), EB.a6()), G, H, U, V)


out = []
for b in flag:
    out.append(encode_byte(b))

print(out)
