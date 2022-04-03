'''
2   bag of fruit, mixed, dried
1   bag prunes
2   litre of water
1   spoon of clove
1/2 lemon

'''

p = random_prime(2^512)
R.<x> = PolynomialRing(GF(p))

def F(f: R, k: Integer) -> R:
    g = x
    while k > 0:
        if k % 2 == 1:
            g = f(g)
        k = k // 2
        f = f(f)
    return g

f = (1*x+2)/(3*x+4)
g = (2*x+1)/(13*x+37)

x0, x1 = randint(0, 2^128), randint(0, 2^128)
y0, y1 = randint(0, 2^128), randint(0, 2^128)

A = F(f, x0)(F(g, x1))
B = F(f, y0)(F(g, y1))
C = F(f, x0 + y0)(F(g, x1 + y1))

with open("output.txt", "w") as f:
    f.write("p = %s\n" % p)
    f.write("A = %s\n" % A)
    f.write("B = %s\n" % B)

print("My kompot is ready: midnight{%d}" % (C(0)))
