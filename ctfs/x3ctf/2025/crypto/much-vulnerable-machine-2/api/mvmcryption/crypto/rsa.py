from dataclasses import dataclass

from Crypto.Hash import SHA256

HASH_LEN = SHA256.digest_size
assert HASH_LEN == 32
HASH_BITS = SHA256.digest_size * 8
assert HASH_BITS == 256


@dataclass
class PrivKey:
    p: int
    q: int
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


@dataclass
class RSA:
    priv: PrivKey

    def verify(self, m, sig):
        m_calc = int(pow(int(sig), int(self.priv.e), int(self.priv.n))).to_bytes(
            HASH_LEN, "big"
        )
        return m_calc == SHA256.new(m).digest()

    def sign(self, m):
        """Sign msg."""
        m = SHA256.new(m).digest()
        m = int.from_bytes(m, "big")
        return pow(m, self.priv.d, self.priv.n)
