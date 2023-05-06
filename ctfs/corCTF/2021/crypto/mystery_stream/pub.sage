R.<x> = PolynomialRing(GF(2), 'x')
poly = [REDACTED]
assert poly.degree() == 64
M = [poly.list()[1:]]
for i in range(63):
	M.append([1 if j == i else 0 for j in range(64)])
M = Matrix(GF(2), M)
A = M^[REDACTED]
E, S = A.eigenspaces_right(format='galois')[0]
assert E == 1
keyvec = S.random_element()
key = int(''.join([str(d) for d in keyvec]), 2)
print(key)
