from random import SystemRandom

random = SystemRandom()
Ds = [11, 19, 43, 67, 163]

def gen_curve(bits=256):
    D = random.choice(Ds)
    H = hilbert_class_polynomial(-D)
    poly = lambda m : D * m * (m+1) + (D+1) // 4
    m_bit = (bits - D.nbits()) // 2 + 1

    while True:
        m = random.getrandbits(m_bit)
        p = poly(m)
        if p.is_prime() and p.nbits() == bits:
            pf = GF(p)
            for j in pf['x'](H).roots(multiplicities=False):
                if j not in [0, pf(1728)]:
                    k = j / (1728 - j)
                    c = pf.random_element()
                    a = 3 * k * c ** 2
                    b = 2 * k * c ** 3
                    E = EllipticCurve(pf, [a, b])
                    # mysterious...
                    if E.trace_of_frobenius() == 1:
                        return E, p