def G_add(A, B):
    x1, y1 = A
    x2, y2 = B
    return ((x1*x2 + D*y1*y2) % p, (x1*y2 + x2*y1 + 2*y1*y2) % p)

def G_mul(A, k):
    out = (1, 0)
    while k > 0:
        if k & 1:
            out = G_add(out, A)
        A = G_add(A, A)
        k >>= 1
    return out

def rand_element():
    while True:
        x = randint(1, p-1)
        d = x^2 * (D + 1) - D
        if (x & 1 == d & 1) and kronecker(d, p) == 1:
            y = (x + sqrt(Zmod(p)(d))) * inverse_mod(D, p) % p
            return (x, y)

D = 13337
p = 17568142778435152362975498611159042138909402642078949814477371651322179417849164549408357464774644525711780515232117470272550677945089719112177956836141583
assert p.nbits() >= 512
assert ((p-1)//2).is_prime() # safe prime

FLAG = open('flag.txt', 'rb').read().strip()
assert len(FLAG) % 8 == 0
M = [int.from_bytes(FLAG[i:i+8], 'big') for i in range(0, len(FLAG), 8)]

G = [rand_element() for _ in M]
c = (1, 0)
for m, gi in zip(M, G):
    c = G_add(c, G_mul(gi, m))

print(f'{D = }')
print(f'{p = }')
print(f'{G = }')
print(f'{c = }')
