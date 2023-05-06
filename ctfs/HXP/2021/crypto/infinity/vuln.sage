#!/usr/bin/env sage
proof.all(False)

if sys.version_info.major < 3:
    print('nope nope nope nope | https://hxp.io/blog/72')
    exit(-2)

ls = list(prime_range(3,117))
p = 4 * prod(ls) - 1
base = bytes((int(p).bit_length() + 7) // 8)

R.<t> = GF(p)[]

def montgomery_coefficient(E):
    a,b = E.short_weierstrass_model().a_invariants()[-2:]
    r, = (t**3 + a*t + b).roots(multiplicities=False)
    s = sqrt(3*r**2 + a)
    return -3 * (-1)**is_square(s) * r / s

def csidh(pub, priv):
    assert type(pub) == bytes and len(pub) == len(base)
    E = EllipticCurve(GF(p), [0, int.from_bytes(pub,'big'), 0, 1, 0])
    assert (p+1) * E.random_point() == E(0)
    for es in ([max(0,+e) for e in priv], [max(0,-e) for e in priv]):
        while any(es):
            x = GF(p).random_element()
            try: P = E.lift_x(x)
            except ValueError: continue
            k = prod(l for l,e in zip(ls,es) if e)
            P *= (p+1) // k
            for i,(l,e) in enumerate(zip(ls,es)):
                if not e: continue
                k //= l
                phi = E.isogeny(k*P)
                E,P = phi.codomain(), phi(P)
                es[i] -= 1
        E = E.quadratic_twist()
    return int(montgomery_coefficient(E)).to_bytes(len(base),'big')

################################################################

randrange = __import__('random').SystemRandom().randrange
class CSIDH:
    def __init__(self):
        self.priv = [randrange(-2,+3) for _ in ls]
        self.pub = csidh(base, self.priv)
    def public(self): return self.pub
    def shared(self, other): return csidh(other, self.priv)

################################################################

alice = CSIDH()

__import__('signal').alarm(600)

from Crypto.Hash import SHA512
secret = ','.join(f'{e:+}' for e in alice.priv)
stream = SHA512.new(secret.encode()).digest()
flag = open('flag.txt','rb').read().strip()
assert len(flag) <= len(stream)
print('flag:', bytes(x^^y for x,y in zip(flag,stream)).hex())

seen = set()
for _ in range(500):
    bob = bytes.fromhex(input().strip())
    assert bob not in seen; seen.add(bob)
    print(alice.shared(bob).hex())

