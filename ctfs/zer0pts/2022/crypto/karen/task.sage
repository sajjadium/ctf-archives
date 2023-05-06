with open("flag.txt", "rb") as f:
    flag = int.from_bytes(f.read(), "big")

n = 70
m = flag.bit_length()
assert n < m
p = random_prime(2**512)


F = GF(p)
x = random_matrix(F, 1, n)
A = random_matrix(ZZ, n, m, x=0, y=2)
A[randint(0, n-1)] = vector(ZZ, Integer(flag).bits())
h = x*A

print(p)
print(list(h[0]))
