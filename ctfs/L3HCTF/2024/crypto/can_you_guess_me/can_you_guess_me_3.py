from Crypto.Util.number import *
from random import *
from secret import flag

q = getPrime(128)

n = 5
T = 2**48
E = 2**32

t = [randint(1,T) for i in range(n)]
e = [randint(1,E) for i in range(n)]
a = [(t[i] * flag - e[i]) % q for i in range(n)]

print('q =', q)
print('a =', a)

flag = "L3HSEC{" + hex(flag)[2:] + "}"

print('flag =', flag)

# q = 313199526393254794805899275326380083313
# a = [258948702106389340127909287396807150259, 130878573261697415793888397911168583971, 287085364108707601156242002650192970665, 172240654236516299340495055728541554805, 206056586779420225992168537876290239524]