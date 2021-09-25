from string import ascii_lowercase, digits
CHARSET = "DUCTF{}_!?'" + ascii_lowercase + digits
n = len(CHARSET)

def encrypt(msg, f):
    ct = ''
    for c in msg:
        ct += CHARSET[f.substitute(CHARSET.index(c))]
    return ct

P.<x> = PolynomialRing(GF(n))
f = P.random_element(6)

FLAG = open('./flag.txt', 'r').read().strip()

enc = encrypt(FLAG, f)
print(enc)
