p, q = [random_prime(2^512, lbound = 2^511) for _ in range(2)]
e = 3

while gcd(p - 1, e) != 1: p = next_prime(p)
while gcd(q - 1, e) != 1: q = next_prime(q)

n = p*q
d = inverse_mod(e, (p-1)*(q-1))

# d stands for debug. You don't even know n, so I don't risk anything.
print('d =', d)

m = ZZ(int.from_bytes(b"It is UNBREAKABLE, I tell you!! I'll even bet a flag on it, here it is: idek{REDACTED}", 'big'))
t = ZZ(int.from_bytes(b"ECRSA offers added security by elliptic entropy.", 'big'))
ym = randint(1, n)
yt = 2

# I like it when my points lie on my curve.
a, b = matrix([[m, 1], [t, 1]]).solve_right([ym^2 - m^3, yt^2 - t^3])
E = EllipticCurve(Zmod(n), [a, b])
M = E(m, ym)
T = E(t, yt)

E.base_field = E.base_ring # fix multiplication over rings (might not work depending on sage version!)
print('Encrypted flag:', M*e)
print('Encrypted test:', T*e)