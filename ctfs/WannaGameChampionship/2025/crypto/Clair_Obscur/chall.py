from sage.all import *
from Crypto.Util.number import bytes_to_long

class CO:
    def __init__(self, p: int, G: list[int], O: list[int]):
        assert is_prime(p)
        assert p.bit_length() == 256
        self.Fp = GF(p)
        self.G = [self.Fp(c) for c in G]
        self.O = [self.Fp(c) for c in O]
        assert self.is_on_curve(self.G)
        assert self.is_on_curve(self.O)

        self.L = self.random_element_from_basis(matrix(self.Fp, [self.G, self.O]).right_kernel_matrix())

    def random_element_from_basis(self, M):
        val = 0
        n = M.nrows()
        Fp = M.base_ring()
        for i in range(n):
            val += Fp.random_element() * M[i]
        return val
    
    def random_point(self):
        while True:
            a, b, c = [self.Fp.random_element() for _ in range(3)]
            x = self.Fp["d"].gen()
            f = a * b**2 + b * c**2 + c * x**2 + x * a**2
            r = f.roots()
            if len(r) > 0:
                d = r[0][0]
                assert self.is_on_curve([a, b, c, d])
                return [a, b, c, d]

    def is_on_curve(self, G: list):
        return G[0] * G[1]**2 + G[1] * G[2]**2 + G[2] * G[3]**2 + G[3] * G[0]**2 == 0

    def neg(self, P: list):
        if P == self.O:
            return P
        
        return self.intersect(P, self.O)
    
    def intersect(self, P: list, Q: list):
        aa = P[0] - Q[0]
        bb = P[1] - Q[1]
        cc = P[2] - Q[2]
        dd = P[3] - Q[3]
        A = aa * bb**2 + bb * cc**2 + cc * dd**2 + dd * aa**2
        C =   (P[1]**2 + 2 * P[0] * P[3]) * aa \
            + (P[2]**2 + 2 * P[0] * P[1]) * bb \
            + (P[3]**2 + 2 * P[1] * P[2]) * cc \
            + (P[0]**2 + 2 * P[2] * P[3]) * dd
        t = -C / A
        R = [0] * 4
        R[0] = P[0] + t * aa
        R[1] = P[1] + t * bb
        R[2] = P[2] + t * cc
        R[3] = P[3] + t * dd

        return R
    
    def add(self, P: list, Q: list):
        if P == self.O:
            return Q
        if Q == self.O:
            return P
        if P == self.neg(Q):
            return self.O
        R = self.intersect(P, Q)
        return self.neg(R)
    
    def double(self, P: list):
        Fa = 2 * P[0] * P[3] + P[1]**2
        Fb = 2 * P[0] * P[1] + P[2]**2
        Fc = 2 * P[1] * P[2] + P[3]**2
        Fd = 2 * P[2] * P[3] + P[0]**2
        vb = Matrix(self.Fp, [[Fa, Fb, Fc, Fd], self.L]).right_kernel_matrix()
        vx, vy, vz, vw = self.random_element_from_basis(vb)

        C3 = vx * vy**2 + vy * vz**2 + vz * vw**2 + vw * vx**2
        C2 =  P[0] * (2 * vw * vx + vy**2) \
            + P[1] * (2 * vx * vy + vz**2) \
            + P[2] * (2 * vy * vz + vw**2) \
            + P[3] * (2 * vw * vz + vx**2)
        t = -C2 / C3

        R = [0] * 4
        R[0] = P[0] + t * vx
        R[1] = P[1] + t * vy
        R[2] = P[2] + t * vz
        R[3] = P[3] + t * vw

        return self.neg(R)
    
    def scalarmult(self, k: int):
        assert k > 0
        R = None
        Q = self.G
        while k > 0:
            if k & 1:
                if R is None:
                    R = Q
                else:
                    R = self.add(R, Q)
            Q = self.double(Q)
            k >>= 1
        return R

flag = open("flag.txt", "r").read()
assert len(flag) == 36
assert flag[:3] == "W1{"
assert flag[-1] == "}"
flag = bytes_to_long(flag[3:-1].encode())

p = int(input("p = "))
G = [int(c) for c in input("G = ").split(",")]
O = [int(c) for c in input("O = ").split(",")]

curve = CO(p, G, O)
print(f"P = {curve.scalarmult(flag)}")