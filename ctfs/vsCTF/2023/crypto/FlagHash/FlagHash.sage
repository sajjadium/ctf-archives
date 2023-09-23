import string
flag = open('flag.txt').read().strip().encode()
F = GF(127^29, 'x', modulus=list(flag))
FlagHash = lambda s: bytes((F(list(s.encode()))^128).polynomial()[:20]).hex()
    
for _ in range(1337):
    s = ''.join(sample(string.ascii_letters + string.digits, randint(13,37)))
    print(s, FlagHash(s))
