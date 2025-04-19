import os
with open("flag.txt", "rb") as f:
        flag = f.read()
flag = os.urandom(4) + flag + os.urandom(4)
bits = 512
assert len(flag) <= bits // 8 and b"UMASS" in flag
p = random_prime(2^(bits + 1), lbound=2^bits)
degree = 100
R.<x> = PolynomialRing(ZZ)
roots = [randrange(p) for _ in range(degree - 1)] + [int.from_bytes(flag, byteorder='big')]
random_poly = randrange(p) * prod([(x - root) for root in roots])
secret_sharing_polynomial = R([c % (2 ^ bits) for c in random_poly.list()])
print("Welcome to our super secure secret sharing function! Get your keys now before they run out!")
for _ in range(degree + 3):
        value = int(input("value: "))
        print(secret_sharing_polynomial(value) % p)
print("Thank you for using our service!")