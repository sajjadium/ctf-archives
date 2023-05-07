from itertools import groupby
from Crypto.Util.number import *
from enum import Enum
from base64 import b64encode
from secret import flag

import plotly.express as px
import random


class State(Enum):
    # PicoChip power states for hardware simulation.
    FALLBACK = 0x0
    SUCCESS = 0x1
    ERROR = 0x2


class PicoChip:
    def __init__(self, k: int, N: int, t: int):
        self.states = []
        self.k = k
        self.N = N
        self.t = t
        self.r = self.gen_op()

    def rec(self, s: State):
        self.states.append(s)

    def gen_op(self) -> list:
        rs = []
        i = 3
        while len(rs) < self.N:
            if isPrime(i):
                self.rec(State.SUCCESS)
                rs.append(i)
            i += 2
        return rs
    
    def gen_secure_prime(self) -> int:
        # More secure than getPrime() as indicated from my latest paper.
        while True:
            v0 = random.randint(2**(self.k-1), 2**self.k)
            v = v0 + 1 - v0 % 2
            while True:
                is_prime = True
                i = 0
                while i < self.N:
                    if v % self.r[i] == 0:
                        v = v + 2
                        self.rec(State.FALLBACK)
                        break
                    i += 1
                    self.rec(State.SUCCESS)

                if i == self.N:
                    for m in range(1, self.t+1):
                        if not miller_rabin(v):
                            is_prime = False
                            v = v + 2
                            self.rec(State.FALLBACK)
                            break
                        self.rec(State.SUCCESS)
                    if is_prime:
                        return v
    
    def plot(self):
        # For transparency, I will show you the internals of PicoChip.
        power_states(self.states)


def power_states(states: list):
    if State.ERROR in states:
        raise Exception("PicoChip is broken!")
    
    power = []
    for k, g in groupby(states):
        if k != State.FALLBACK:
            power.append(sum(1 for _ in g))
        else:
            power.extend([0 for _ in g])

    gx, gy = [], []
    for i in range(len(power)):
        gx.append(i)
        gy.append(power[i])
        gx.append(i + 1)
        gy.append(power[i])

    fig = px.line(x=gx, y=gy, title="PicoChip Power States")
    fig.write_html("power_states.html")


def miller_rabin(n: int) -> bool:
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    
    d = n - 1
    while d % 2 == 0:
        d //= 2
    a = 2 + random.randint(1, n - 4)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    
    while d != n-1:
        x = (x * x) % n
        d *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False


if __name__ == "__main__":
    pico = PicoChip(36, 60, 1)
    p = pico.gen_secure_prime()
    q = pico.gen_secure_prime()
    assert p != q and isPrime(p) and isPrime(q)

    assert flag.startswith(b"cvctf{") and flag.endswith(b"}")
    flag = flag[6:-1]
    
    N = p * q
    e = 0x10001
    m = bytes_to_long(flag)
    ct = pow(m, e, N)

    print("[+] PicoChip Encryption Parameters:")
    # print(f"N = {N}")
    print(f"e = {e}")
    print(f"ct = {ct}")

    pico.plot()
    print("[+] PicoChip Power States saved.")