from random import choice, shuffle, randint

def as_poly_of(self, gen):
    L = self.parent()
    d = L.degree()
    V = L.base_ring()^d

    vecs = [vector(self)] + [vector(gen^i) for i in range(d)]
    dependence = V.linear_dependence(vecs)

    if all(coeffs[0] == 0 for coeffs in dependence):
        raise ArithmeticError(f'Cannot express {self} as a polynomial in {gen}')

    coeffs = next(list(coeffs) for coeffs in dependence if coeffs[0] != 0)
    return L.base_ring()['x'](coeffs[1:])/-coeffs[0]

def randomize(message, bits):
    L = GF(127)
    for i in range(bits.nbits() -1):
        L = L['x'].irreducible_element(2, algorithm='random').splitting_field(f't{i}')

    M = sum(c*L.gen()^i for i, c in enumerate(message))

    for _ in range(randint(1, bits.nbits())):
        m = M
        while m == M:
            roots = L.random_element().minimal_polynomial().roots(L)
            shuffle(roots)

            try:
                (r1, _), (r2, _) = roots[:2]
                M = as_poly_of(M, r1)(r2)
            except:
                pass

    return bytes(map(int, M.polynomial().padded_list(L.degree())))

if __name__ == '__main__':
    from sys import argv
    if len(argv) < 2:
        print('Usage: sage main.sage <flag>')
        exit()

    flag = argv[1].encode()
    assert len(flag) % 16 == 0

    flag = [flag[i:i+16] for i in range(0, len(flag), 16)]
    shuffle(flag)

    for part in flag:
        print(randomize(part, 32).hex(), end='')
    print()