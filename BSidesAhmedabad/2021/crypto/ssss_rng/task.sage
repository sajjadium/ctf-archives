p = random_prime(1<<512)

a = randint(2, p-1)
b = randint(2, p-1)
x = randint(2, p-1)

def g():
    global a, b, x
    x = (a*x + b) % p
    return x

with open("flag.txt", "rb") as f:
    flag = int.from_bytes(f.read().strip(), "big")
assert flag < p

PR.<X> = PolynomialRing(GF(p))
f = g() + g()*X + g()*X**2 + g()*X**3 + g()*X**4 + g()*X**5
vs = [(i, f(i)) for i in range(1, 5)]

print(p)
print(vs)
print(f(flag))
