#!/usr/bin/env sage

p = 2
F = GF(p)
P.<x> = PolynomialRing(F)


class Cipher:
    def __init__(self, size, params):
        self.size = size
        self.params = params

    def sequence(self, key):
        while True:
            key = key * self.params[0]
            yield key + self.params[1]

    def encrypt(self, key, data, strength):
        for value, pbit in zip(self.sequence(key), data):
            xbit = sum(value[i] for i in range(0, strength, 2))
            ybit = mul(value[i] for i in range(1, strength, 2))
            
            yield int(pbit) ^^ int(xbit) ^^ int(ybit)


def main():
    size = 256
    length = 1024
    strength = 10

    q = P.irreducible_element(size, 'minimal_weight')
    R.<x> = P.quo(q)

    key, a, b = [R.random_element() for _ in range(3)]

    with open('flag.txt', 'rb') as file:
        flag = file.read().strip()

    message = int.from_bytes(flag, 'big')
    assert message.bit_length() < size
    plaintext = list(map(int, bin(message)[2:]))
    padding = [0] * (length - len(plaintext))

    cipher = Cipher(size, [a, b])
    ciphertext = list(cipher.encrypt(key, padding + plaintext, strength))
    result = int(''.join(map(str, ciphertext)), 2)

    print(a)
    print(b)
    print(result)


if __name__ == '__main__':
    main()
