import hashlib


SEP = 'ZProof'

def generate_primes(n):
    num = 3
    primes = [2]
    while len(primes) < n:
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 2
    return primes

NUML = 18
try:
    with open('PRIMES.cache', 'r') as f:
        PRIMES = [int(n) for n in f.read().strip().split(' ')]
except FileNotFoundError:
    PRIMES = generate_primes(1 << NUML)
    open('PRIMES.cache', 'w').write(' '.join(map(str, PRIMES)))

TOTAL_PRIME_BITS = 0
for p in PRIMES:
    TOTAL_PRIME_BITS += p.bit_length() - 1

BITS = 50_000                              # maximum norm, bits
SECP = 256                                 # \secpar
RATE = (TOTAL_PRIME_BITS + BITS - 1)//BITS # rate
SECB = RATE.bit_length() - 1               # security bits per query
QUERIES = (SECP + SECB - 1) // SECB        # total number of queries
assert len(PRIMES) == 1 << NUML

def sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

class Merkle:
    def __init__(self, data):
        assert len(data) and (len(data) & (len(data) - 1)) == 0

        if len(data) == 1:
            self.size = 1
            self.leaf = data[0]
            self.root = sha256(data[0])
        else:
            mid = len(data)//2
            self.lhs = Merkle(data[:mid])
            self.rhs = Merkle(data[mid:])
            self.leaf = None
            self.root = sha256(self.lhs.root + self.rhs.root)
            self.size = len(data)

    def open(self, pos):
        assert 0 <= pos < self.size

        if self.size == 1:
            return [self.leaf]

        assert self.size % 2 == 0
        mid = self.size // 2
        if pos >= mid:
            prf = self.rhs.open(pos - mid)
            prf.append((1, self.lhs.root))
            return prf
        else:
            prf = self.lhs.open(pos)
            prf.append((0, self.rhs.root))
            return prf

def verify(root: str, proof: list, pos: int, size: int) -> bytes:
    assert len(proof) > 0
    assert len(proof) < 32

    lvls = len(proof) - 1
    assert 1 << lvls == size

    leaf = proof[0]
    node = sha256(leaf)

    for i in range(1, lvls+1):
        (dirc, sibl) = proof[i]
        assert isinstance(sibl, str)
        assert isinstance(dirc, int)
        assert len(sibl) == 64
        assert dirc in [0, 1]
        if dirc == 0:
            node = sha256(node + sibl)
        else:
            node = sha256(sibl + node)

    assert node == root
    return leaf

class ModVec:
    def __init__(self, vec, mod):
        assert len(mod) == len(vec)
        self.vec = vec
        self.mod = mod

    def __add__(self, other):
        if isinstance(other, int):
            return ModVec([(a + other) % p for a, p in zip(self.vec, self.mod)], self.mod)
        elif isinstance(other, ModVec):
            assert self.mod == other.mod
            return ModVec([(a + b) % p for a, b, p in zip(self.vec, other.vec, self.mod)], self.mod)
        else:
            return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            return ModVec([(a - other) % p for a, p in zip(self.vec, self.mod)], self.mod)
        elif isinstance(other, ModVec):
            assert self.mod == other.mod
            return ModVec([(a - b) % p for a, b, p in zip(self.vec, other.vec, self.mod)], self.mod)
        else:
            return NotImplemented

    def __rsub__(self, other):
        return ModVec([(other - a) % p for a, p in zip(self.vec, self.mod)], self.mod)

    def __mul__(self, other):
        if isinstance(other, int):
            return ModVec([(a * other) % p for a, p in zip(self.vec, self.mod)], self.mod)
        elif isinstance(other, ModVec):
            assert self.mod == other.mod
            return ModVec([(a * b) % p for a, b, p in zip(self.vec, other.vec, self.mod)], self.mod)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def check_equal(self, v: int):
        rdc = [v % p for p in self.mod]
        assert self.vec == rdc, f"Expected {rdc} but got {self.vec}"

class Comm(Merkle):
    def __init__(self, n: int):
        self.n = n
        self.cord = [n % p for p in PRIMES]
        super().__init__([str(n) for n in self.cord])

    def eval(self):
        return self.n

class CommExpr:
    def __init__(self, com, poss, open):
        assert len(poss) == QUERIES
        assert len(open) == QUERIES
        self.poss = poss
        self.open = open
        self.root = com

        # verify all the openings
        values = []
        for pos, pf in zip(poss, open):
            assert pos < len(PRIMES)
            values.append(int(verify(com, pf, pos, len(PRIMES))))
        self.value = ModVec(values, [PRIMES[i] for i in poss])

    def eval(self):
        return self.value

class Mul:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def eval(self):
        if isinstance(self.lhs, int):
            lhs_val = self.lhs
        else:
            lhs_val = self.lhs.eval()

        if isinstance(self.rhs, int):
            rhs_val = self.rhs
        else:
            rhs_val = self.rhs.eval()

        return lhs_val * rhs_val

    def __repr__(self):
        return f'Mul({self.lhs}, {self.rhs})'

class Add:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def eval(self):
        if isinstance(self.lhs, int):
            lhs_val = self.lhs
        else:
            lhs_val = self.lhs.eval()

        if isinstance(self.rhs, int):
            rhs_val = self.rhs
        else:
            rhs_val = self.rhs.eval()

        return lhs_val + rhs_val

    def __repr__(self):
        return f'Add({self.lhs}, {self.rhs})'

class Transcript:
    def __init__(self, statement):
        self.hsh = sha256(SEP + ":" + str(statement))

    def com(self, com):
        self.hsh = sha256(self.hsh + com.root)

    def value(self, n: int):
        self.hsh = sha256(self.hsh + str(n))

    def challenge(self) -> int:
        self.hsh = sha256(self.hsh)
        return int(self.hsh, 16)

class Prover:
    def __init__(self, statement):
        self.tx = Transcript(statement)
        self.coms = []
        self.open = []
        self.vals = []

    def equal(self, expr, value):
        assert expr.eval() == value, f"Expected {value} to equal {expr.eval()}"

    def com(self, n: int):
        com = Comm(n)
        self.coms.append(com)
        self.tx.com(com)
        return com

    def value(self, value: int):
        self.tx.value(value)
        self.vals.append(int(value))
        return value

    def combine(self):
        expr = Mul(self.tx.challenge(), self.coms[0])
        for com in self.coms[1:]:
            expr = Add(expr, Mul(self.tx.challenge(), com))
        return expr

    def finalize(self):
        cmb = self.combine()
        value = self.value(cmb.eval())
        self.equal(cmb, value)

        # opening proofs
        positions = [self.tx.challenge() % len(PRIMES) for _ in range(QUERIES)]
        return {
            'root': [com.root for com in self.coms],
            'vals': self.vals,
            'open': [[com.open(pos) for pos in positions] for com in self.coms],
            'poss': positions
        }

class Verifier:
    def __init__(self, proof, statement):
        self.tx = Transcript(statement)
        self.poss = proof['poss']
        self.vals = iter(proof['vals'])
        self.exprs = []

        root = proof['root']
        open = proof['open']

        assert len(open) == len(root)
        assert len(self.poss) == QUERIES

        # construct comm expr
        self.coms = []
        for root, open in zip(root, open):
            assert len(root) == 64
            assert len(open) == len(self.poss)
            self.coms.append(CommExpr(root, self.poss, open))
        self.seq_coms = iter(self.coms)

    def value(self):
        value = next(self.vals)
        assert - 2**BITS < value < 2**BITS
        self.tx.value(value)
        return value

    def equal(self, expr, value):
        self.exprs.append((expr, value))

    def com(self):
        com = next(self.seq_coms)
        assert isinstance(com, CommExpr)
        self.tx.com(com)
        return com

    def combine(self):
        expr = Mul(self.tx.challenge(), self.coms[0])
        for com in self.coms[1:]:
            expr = Add(expr, Mul(self.tx.challenge(), com))
        return expr

    def finalize(self):
        # add the random linear combination
        cmb = self.combine()
        value = self.value()
        self.equal(cmb, value)

        # check positions
        assert self.poss == [self.tx.challenge() % len(PRIMES) for _ in range(QUERIES)]

        # check all expressions
        for expr, value in self.exprs:
            expr.eval().check_equal(value)

def sub(a, b):
    return Add(a, Mul(b, -1))

def equal(rel, a, b):
    rel.equal(sub(a, b), 0)

def square(v):
    return Mul(v, v)

def four(v1, v2, v3, v4):
    return Add(
        Add(
            square(v1),
            square(v2),
        ),
        Add(
            square(v3),
            square(v4)
        )
    )

# relation to prove:
# p \notin {-1, 1}
# q \notin {-1, 1}
# p * q = N
#
# via:
# a^2 - 4 >= 0 <=> a \notin {-1, 1}
# b^2 - 4 >= 0 <=> b \notin {-1, 1}
#
# arithmetic circuit:
# p * q = N
# a1^2 + a2^2 + a3^2 + a4^2 = p^2 - 4
# b1^2 + b2^2 + b3^2 + b4^2 = q^2 - 4
def rel_factor(
    rel,
    p, a1, a2, a3, a4,
    q, b1, b2, b3, b4,
    N,
):
    rel.equal(Mul(p, q), N)
    a = Add(square(p), -4)
    b = Add(square(q), -4)
    equal(rel, a, four(a1, a2, a3, a4))
    equal(rel, b, four(b1, b2, b3, b4))
