#!/usr/bin/env python3

import random
import base64

VALUESIZE = 216
BLOCKSIZE = 16

class Value:
    def __init__(self, n):
        if isinstance(n, Value):
            n = n.n
        if not (isinstance(n, int) and 0 <= n <= VALUESIZE):
            raise ValueError
        self.n = n

    def __eq__(self, other):
        return self.n == other.n

    def extract(self):
        a = self.n % 3
        b = ((self.n // 27) + 1) % 3
        c = (self.n // 9) % 3
        d = (((self.n // 27) + 1) // 3) % 3
        if b == 0:
            f = (self.n // 3) % 3
            e = (2 * d) % 3
        else:
            e = (self.n // 3) % 3
            f = ((1 + d*e) * b) % 3
        return a,b,c,d,e,f

    @classmethod
    def assemble(cls, a, b, c, d, e, f):
        for x in (a,b,c,d,e,f):
            if not (isinstance(x, int) and 0 <= x <= 2):
                raise ValueError
        n = 0
        n += a
        n += 27 * ((b + 3 * d) - 1)
        n += 9 * c
        if b == 0:
            n += 3 * f
        else:
            n += 3 * e
        return Value(n)

    def __add__(self, other):
        sa, sb, sc, sd, se, sf = self.extract()
        oa, ob, oc, od, oe, of = other.extract()
        a = (sa + sb * oa + sd * oc) % 3
        b = (sb * ob + sd * oe) % 3
        c = (sc + se * oa + sf * oc) % 3
        d = (sb * od + sd * of) % 3
        e = (se * ob + sf * oe) % 3
        f = (se * od + sf * of) % 3
        return Value.assemble(a, b, c, d, e, f)

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return repr(self.n)

class DreamHash:
    def __init__(self):
        # I read that it is important to use nothing-up-my-sleeves-numbers for
        # constants in cryptosystems, so I generate the template randomly.
        self.template = [
                random.sample(
                    sum([[(i+j) % BLOCKSIZE]*(1 if j == 0 else j*VALUESIZE)
                         for j in range(BLOCKSIZE)], []),
                    k=(1 + VALUESIZE * sum(range(BLOCKSIZE)))
                    )
                for i in range(BLOCKSIZE)
                ]

    def hash(self, data):
        unfolded_data = [Value(d) for d in data]
        unfolded_data += [Value(0)] * (BLOCKSIZE - (len(unfolded_data) % BLOCKSIZE))
        folded_data = [sum(unfolded_data[i::BLOCKSIZE], Value(0)) for i in range(BLOCKSIZE)]
        result = []
        for i in range(BLOCKSIZE):
            result.append(Value(0))
            for j in self.template[i]:
                result[-1] += folded_data[j]
        return [x.n for x in result]

def main():
    print('Welcome to the DreamHash testing service.')
    H = DreamHash()
    secret = bytes([random.randrange(VALUESIZE) for _ in range(BLOCKSIZE)])
    print('I generated a secret. Can you recover it?')
    for _ in range(4):
        try:
            user_bytes = base64.b64decode(input('Your values: '))
            h = H.hash(secret + user_bytes)
            print(f'Hash: {base64.b64encode(bytes(h)).decode()}')
        except:
            exit(0)
    user_bytes = base64.b64decode(input('Your guess at secret: '))
    if user_bytes == secret:
        with open('flag.txt', 'r') as f:
            print(f.read())
    else:
        print('Wrong.\n')


if __name__ == '__main__':
    main()
