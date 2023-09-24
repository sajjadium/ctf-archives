from sage.all import *
import hashlib
P = Permutations(256).random_element()
print(P**2)
print([x^y for x,y in zip(hashlib.sha512(str(P).encode()).digest(), open('flag.txt', 'rb').read())])
