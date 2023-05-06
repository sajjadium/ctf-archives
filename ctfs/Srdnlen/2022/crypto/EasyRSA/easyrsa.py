#!/usr/bin/env python3

from Crypto.Util.number import getPrime, bytes_to_long


def padding(text, n):
    for j in range(n % 2**8):
        text += b"poba"
    return bytes_to_long(text)


if __name__ == '__main__':
    f = open('flag.txt', 'r').read().encode()
    e = 13

    print("Can u break the best encryption tool of the world?")
    print()

    nums = []

    for i in range(15):
        x, y = getPrime(16), getPrime(16)
        print(f"x*y:{x * y}")
        k = int(input("Give me a number:"))
        if k < 2 ** 128 or k in nums or k % (x * y) == 0:
            print("Are u serious?")
            exit(1)
        r = int(input("Give me another number:"))
        if r < 2 ** 128 or r in nums:
            print("Are u serious?")
            exit(1)
        nums += [k, r]
        print()
        N = getPrime(512) * getPrime(512)
        CT = pow(padding(f, pow(k, r, x * y)), e, N)
        print(f"e:{e}")
        print(f"N:{N}")
        print(f"CT:{CT}")
        print()
