class R_MT19937_32bit:
    def __init__(self, seed=0):
        self.f = 1812433253
        (self.w, self.n, self.m, self.r) = (32, 624, 397, 31)
        (self.u, self.s, self.t, self.l)= (11, 7, 15, 18)
        (self.a, self.b, self.c) = (0x9908b0df, 0x9d2c5680, 0xefc60000)
        (self.lower, self.upper, self.d) = (0x7fffffff, 0x80000000, 0xffffffff)
        self.MT = [0 for i in range(self.n)]
        self.seedMT(seed)

    def seedMT(self, seed):
        num = seed
        self.index = self.n
        for _ in range(0,51):
            num = 69069 * num + 1
        g_prev = num
        for i in range(self.n):
            g = 69069 * g_prev + 1
            self.MT[i] = g & self.d
            g_prev = g
        
        return self.MT

    def twist(self):
        for i in range(0, self.n):
            x = (self.MT[i] & self.upper) + (self.MT[(i + 1) % self.n] & self.lower)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0

    def get_num(self):
        if self.index >= self.n:
            self.twist()
        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        self.index += 1
        return y & ((1 << self.w) - 1)
