"""
reimplementation of https://eprint.iacr.org/2021/469.pdf
"""
import os
from dataclasses import dataclass
from hashlib import sha256

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes


flag = os.getenvb(b"FLAG", b"FAKEFLAG{THIS_IS_FAKE}")


@dataclass
class EntropoidParams:
    p: int
    a3: int
    a8: int
    b2: int
    b7: int


@dataclass
class EntropoidPowerIndex:
    a: list[int]
    pattern: list[int]
    base: int


class Entropoid:
    def __init__(self, params: EntropoidParams) -> None:
        self.p = params.p
        self.Fp = GF(self.p)
        self.a3, self.a8, self.b2, self.b7 = (
            self.Fp(params.a3),
            self.Fp(params.a8),
            self.Fp(params.b2),
            self.Fp(params.b7),
        )
        self.a1 = (self.a3 * (self.a8 * self.b2 - self.b7)) / (self.a8 * self.b7)
        self.a4 = (self.a8 * self.b2) / self.b7
        self.b1 = -((self.b2 * (self.a8 - self.a3 * self.b7)) / (self.a8 * self.b7))
        self.b5 = (self.a3 * self.b7) / self.a8

    def __call__(self, x1: int, x2: int) -> "EntropoidElement":
        return EntropoidElement(x1, x2, self)

    def random_power_index(self, base: int) -> EntropoidPowerIndex:
        size = ceil(log(self.p) / log(base))
        a_num = Integer(randrange(1, self.p))
        a = a_num.digits(base, padto=size)
        pattern_num = Integer(randrange(0, (base - 1) ** size - 1))
        pattern = pattern_num.digits(base - 1, padto=size)
        return EntropoidPowerIndex(a=a, pattern=pattern, base=base)


class EntropoidElement:
    def __init__(self, x1: int, x2: int, entropoid: Entropoid) -> None:
        self.entropoid = entropoid
        Fp = entropoid.Fp
        self.x1 = Fp(x1)
        self.x2 = Fp(x2)

    def __mul__(self, other) -> "EntropoidElement":
        e = self.entropoid
        x1 = e.a8 * self.x2 * other.x1 + e.a3 * self.x2 + e.a4 * other.x1 + e.a1
        x2 = e.b7 * self.x1 * other.x2 + e.b2 * self.x1 + e.b5 * other.x2 + e.b1
        return self.entropoid(x1, x2)

    def __repr__(self) -> str:
        return f"({self.x1}, {self.x2})"

    def __eq__(self, other) -> bool:
        return (
            self.entropoid == other.entropoid
            and self.x1 == other.x1
            and self.x2 == other.x2
        )

    def __pow__(self, other: EntropoidPowerIndex) -> "EntropoidElement":
        a, pattern, base = other.a, other.pattern, other.base
        k = len(a)
        w = self
        ws = [w]
        for p_i in pattern[1:]:
            ws.append(calc_r(ws[-1], base, p_i))
        j = a.index(next(filter(lambda x: x != 0, a)))
        a_j = a[j]
        if a_j == 1:
            x = ws[j]
        else:
            wj = ws[j]
            x = calc_r(wj, a_j, pattern[j] % (a_j - 1))
        for i in range(j + 1, k):
            a_i = a[i]
            if a_i == 0:
                continue
            if a_i == 1:
                tmp = ws[i]
            else:
                wi = ws[i]
                tmp = calc_r(wi, a_i, pattern[i] % (a_i - 1))
            if pattern[i - 1] % 2 == 0:
                x = tmp * x
            else:
                x = x * tmp
        return x

    def to_bytes(self) -> bytes:
        p = self.entropoid.p
        assert p.bit_length() % 8 == 0
        size = p.bit_length() // 8
        return long_to_bytes(int(self.x1), size) + long_to_bytes(int(self.x2), size)


class DH:
    def __init__(self, g: EntropoidElement, base: int) -> None:
        E = g.entropoid
        self.__priv = E.random_power_index(base)
        self.pub = g**self.__priv

    def gen_share(self, other_pub: EntropoidElement) -> EntropoidElement:
        return other_pub**self.__priv


def calc_r(x: EntropoidElement, a: int, i: int) -> EntropoidElement:
    assert 0 <= i <= a - 2

    def calc_to_left(
        y: EntropoidElement, x: EntropoidElement, a: int
    ) -> EntropoidElement:
        res = y
        for _ in range(a):
            res = x * res
        return res

    return calc_to_left((calc_to_left(x, x, i) * x), x, a - i - 2)


def exec_dh(E: Entropoid) -> EntropoidElement:
    g = E(13, 37)
    alice = DH(g, 17)
    bob = DH(g, 33)
    s_ab = alice.gen_share(bob.pub)
    s_ba = bob.gen_share(alice.pub)
    assert s_ab == s_ba
    print(alice.pub, bob.pub)
    return s_ab


if __name__ == "__main__":
    # Check DHKE works correctly by params for debug
    params_debug = EntropoidParams(
        p=18446744073709550147,  # safe prime
        a3=1,
        a8=3,
        b2=3,
        b7=7,
    )
    E_debug = Entropoid(params_debug)
    for _ in range(256):
        exec_dh(E_debug)

    # Generate shared key by DHKE using strong params for production
    params = EntropoidParams(
        p=0xF557D412B06B9370BA144A3FA9E4F519B4263C5232D86089B661A9D957A9DCE371F01AD4E36642F5A6377D80FC195889400EBE9C2AC91E785C841BCC3FC97ECCA78B19962692D9C049876A785F72CB66416BF5FFCF09BB8EE54D5B4501E9FD3ACC7FD87BB3A0163BECC363994C9C91E5B624AC59D032635B5CAE8B9E04FB1056F69E7493D7F00498F8CE98CA535B81FDA18BEF2DB0AE82377BDDEAFBAA1D8FDA157C923D66D1330B149213A2BF56E25755F743BDB2486D976EDF01C91D963481C31B6634A2B9F7FDC9FA63DF5DEC5F55D3BBF28E43863F26A55FD6AD668C9087228464C1D5EE4F83E82869C401568B8C1E6420423CF110091548CBAB57DBE4F7,  # safe prime
        a3=1,
        a8=3,
        b2=3,
        b7=7,
    )
    E = Entropoid(params)
    s_ab = exec_dh(E)
    key = sha256(s_ab.to_bytes()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    enc = cipher.encrypt(pad(flag, 16))
    print(f"enc = {enc.hex()}")
