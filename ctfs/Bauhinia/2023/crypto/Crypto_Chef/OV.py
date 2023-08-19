# Found an Orange Vessel!
# Let's use the seasoning in it too!

import galois # galois is used just because it's more lightweighted when compared to sage 
import numpy as np

class OilVinegar:

    class LFSRSalt:
        def __init__(self, q, water_tap, salt):
            self.GF = galois.GF(2)
            self.q = q
            self.k = self.q.bit_length() - 1
            assert self.q == 2**self.k

            self.water_tap = self.GF(water_tap)
            self.lfsr = galois.FLFSR.Taps(self.GF(water_tap), self.GF([(c >> (self.k - i - 1)) & 1 for c in salt.view(np.ndarray) for i in range(self.k)]))
        
        def step(self, num):
            rtn = []
            for _ in range(num):
                elem = 0
                for _ in range(self.k):
                    elem <<= 1
                    elem |= int(self.lfsr.step(1))
                rtn.append(elem)

            return galois.GF(self.q)(rtn)

    def __init__(self, q, o, v, water_tap, salt, pepper, secret_sauce):
        
        self.o = o
        self.v = v
        self.n = o + v
        self.GF = galois.GF(q)

        self.SS = self.GF(secret_sauce)
        self.pepper = self.GF(pepper)
        self.lfsr_salt = self.LFSRSalt(q, water_tap, self.GF(salt))

        self.F, self.pub = self.genkey()

    def genkey(self):
        F_quad = self.GF.Zeros((self.o, self.n, self.n))
        pub_quad = self.GF.Zeros((self.o, self.n, self.n))

        for i in range(self.o):
            B0 = self.GF.Zeros((self.o, self.o))
            B1 = self.GF.Random((self.o, self.v))
            B2 = self.GF.Random((self.v, self.o))
            B3 = self.GF.Random((self.v, self.v))

            Fi = self.GF(np.block([[B0, B1], [B2, B3]]))
            F_quad[i] = Fi
            pub_quad[i] = self.SS.transpose() @ Fi @ self.SS # matmul

        F_lin = self.GF.Random((self.o, self.n))
        pub_lin = F_lin @ self.SS

        F_const = self.GF.Random(self.o)
        pub_const = F_const.copy()

        return (F_const, F_lin, F_quad), (pub_const, pub_lin, pub_quad)
    
    def findOil(self, vinegar, msg):

        A = self.GF.Zeros((self.o, self.o))
        b = msg.copy()

        for i in range(self.o):

            quadOil = np.sum((self.F[2][i][:self.o, -self.v:] + self.F[2][i].transpose()[:self.o, -self.v:]) * vinegar, axis = 1)
            quadConst = vinegar @ self.F[2][i][-self.v:, -self.v:] @ vinegar

            linOil = self.F[1][i][:self.o]
            linConst = self.F[1][i][-self.v:] @ vinegar

            A[i] = quadOil + linOil
            b[i] -= quadConst + linConst + self.F[0][i]
        
        if np.linalg.matrix_rank(A) < self.o:
            return None
        
        return np.linalg.solve(A, b)

    # Do you know what is msg? msg makes everything good. If your dish is not delicious, add msg.
    # If your life is not good, add msg, it will be a lot better.
    def cook(self, msg):
        assert len(msg) == self.o
        msg = self.GF(msg)

        vinegar = np.append(self.pepper, self.lfsr_salt.step(self.v // 2))
        oil = self.findOil(vinegar, msg)
        while oil is None:
            vinegar = np.append(self.pepper, self.lfsr_salt.step(self.v // 2))
            oil = self.findOil(vinegar, msg)
        
        tastyDish = np.linalg.inv(self.SS) @ np.append(oil, vinegar)

        return tastyDish
    
    # Verify whether you really add the msg in that tasty dish!
    def verify(self, tastyDish, msg):
        tastyDish = self.GF(tastyDish)
        msg = self.GF(msg)

        taste = self.pub[0]
        taste += self.pub[1] @ tastyDish
        for i in range(self.o):
            taste[i] += tastyDish @ self.pub[2][i] @ tastyDish
        
        return np.all(taste == msg)
        