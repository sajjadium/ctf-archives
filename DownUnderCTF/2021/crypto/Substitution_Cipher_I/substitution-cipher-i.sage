def encrypt(msg, f):
    return ''.join(chr(f.substitute(c)) for c in msg)

P.<x> = PolynomialRing(ZZ)
f = 13*x^2 + 3*x + 7

FLAG = open('./flag.txt', 'rb').read().strip()

enc = encrypt(FLAG, f)
print(enc)
