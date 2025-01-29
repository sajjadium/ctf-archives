from dataclasses import dataclass
from secrets import token_bytes

from Crypto.Hash import SHA256
from Crypto.Signature.pss import MGF1
from Crypto.Util.number import getPrime, isPrime

HASH_LEN = SHA256.digest_size
assert HASH_LEN == 32
HASH_BITS = SHA256.digest_size * 8
assert HASH_BITS == 256


def fast_prime(e: int):
    """
    Our CISO mandated we generate primes like this, "apparently" its more efficient and/or faster. (See MVM-7173741 in jira for more on this.)

    We already told our CISO that we'd lose our ISO 27k1 certification if we did stuff like this, as a result he started laughing.
    After about 10min of cynical laughter he finally calmed down, and told us: "We lost that certification as soon as we were audited.".
    """
    while True:
        k = getPrime(int(HASH_BITS * 2 - HASH_LEN * 3.5))
        d = pow(e, -1, k)
        p = 1 + (e * d - 1) // k
        if isPrime(p):
            return p, d


@dataclass
class PrivKey:
    p: int
    q: int
    # See "Customer Retention Strategies" on confluence
    # dp: int
    # dq: int
    e: int

    @property
    def phi(self):
        return (self.p - 1) * (self.q - 1)

    @property
    def d(self):
        return pow(self.e, -1, self.phi)

    @property
    def n(self):
        return self.p * self.q

    @property
    def public_key(self):
        return PubKey(self.n, self.e)

    @property
    def u(self):
        return pow(self.p, -1, self.q)


@dataclass
class PubKey:
    n: int
    e: int


def xor(x, y):
    if len(x) > len(y):
        x, y = y, x
    return bytes([x[i] ^ y[i] for i in range(len(x))]) + y[len(x) :]


@dataclass
class RSA:
    priv: PrivKey

    @classmethod
    def new(cls):
        n_e = HASH_BITS * 4
        e = getPrime(n_e)

        # See "Customer Retention Strategies" on confluence
        p, _ = fast_prime(e)
        q, _ = fast_prime(e)

        return cls(PrivKey(p, q, e))

    def verify(self, m, sig):
        m_pad = int(pow(int(sig), int(self.priv.e), int(self.priv.n))).to_bytes(
            HASH_BITS, "big"
        )
        return self.unpad(m_pad) == SHA256.new(m).digest()

    def unpad(self, m_pad):
        x, y = m_pad[2:-HASH_LEN], m_pad[-HASH_LEN:]
        r = xor(y, MGF1(x, HASH_LEN, SHA256))
        m = xor(x, MGF1(r, HASH_BITS - HASH_LEN - 2, SHA256)).rstrip(b"\x00")
        return m[:-1]

    def pad(self, m):
        """
        This might actually be secure, proving/disproving this is above my paygrade tho.

        In the end, all i need is $5 anyways.
        """
        m += b"\x01" + b"\x00" * (HASH_BITS - HASH_LEN - 3 - len(m))
        r = token_bytes(HASH_LEN)
        x = xor(m, MGF1(r, HASH_BITS - HASH_LEN - 2, SHA256))
        y = xor(r, MGF1(x, HASH_LEN, SHA256))
        m_pad = x + y
        return m_pad

    def sign(self, m):
        m = self.pad(SHA256.new(m).digest())
        m = int.from_bytes(m, "big")
        return pow(m, self.priv.d, self.priv.n)
