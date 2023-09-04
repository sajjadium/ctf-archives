from Crypto.Util.number import bytes_to_long, getStrongPrime, isPrime

SIZE = 512
e = 65537

with open("flag.txt", "rb") as f:
    m = bytes_to_long(f.read())


def encrypt(m):
    while True:
        p = getStrongPrime(SIZE)
        if p % 4 != 3:
            continue
        q = p**2 + 1
        assert q % 2 == 0
        if isPrime(q // 2):
            break

    r = getStrongPrime(SIZE * 3)
    n = p * q * r
    c = pow(m, e, n)
    return n, c

if __name__ == "__main__":
    n0, c0 = encrypt(m)
    n1, c1 = encrypt(c0)
    n2, c  = encrypt(c1)
    
    assert m < n0 and c0 < n1 and c1 < n2

    print(f"{n0 = }")
    print(f"{n1 = }")
    print(f"{n2 = }")
    print(f"{c = }")
