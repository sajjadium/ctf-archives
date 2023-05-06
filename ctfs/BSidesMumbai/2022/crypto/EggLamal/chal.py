from params import a, b, p

FLAG = int(open('flag.txt', 'rb').read().hex(), 16)

g = 2
m = FLAG % p

A = pow(g, a, p)
B = pow(g, b, p)
s = pow(A, b, p)
c = s * m % p

print('p =', p)
print('A =', A)
print('B =', B)
print('c =', c)
