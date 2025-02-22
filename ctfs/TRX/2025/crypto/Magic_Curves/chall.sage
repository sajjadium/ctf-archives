with open('flag.txt', 'r') as f:
    FLAG = f.read().strip()

a, b, p = map(int, input("Give me a, b, p: ").strip().split(','))

assert is_prime(p)
assert 216 <= p.bit_length() <= 256

assert 0 < a < p
assert 0 < b < p
assert a != b

Zp = Zmod(p)

def genPoints(A, B):
    E = EllipticCurve(Zp, [A, B])
    return E.gen(0), E.random_point()

P1, Q1 = genPoints(a, b)
P2, Q2 = genPoints(b, a)

print("Here are your points:", ','.join(map(str, [P1, Q1, P2, Q2])))

k1, k2 = map(int, input("Give me k1, k2: ").strip().split(','))

assert k1 * P1 == Q1
assert k2 * P2 == Q2

print("GG! Here is your flag:", FLAG)