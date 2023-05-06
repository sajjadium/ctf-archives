triangle =[[1]]
flag = open('flag.txt','rb').read()

from Crypto.Util.number import getPrime,bytes_to_long
from math import gcd
p = getPrime(20)
while len(triangle[-1]) <= p:
    r = [1]
    for i in range(len(triangle[-1]) - 1):
        r.append(triangle[-1][i] + triangle[-1][i+1])
    r.append(1)
    triangle.append(r)
code = ''
for x in triangle[-1]:
    code+=str(x%2)
d = int(code,2)
while True:
    P = getPrime(512)
    Q = getPrime(512)
    if gcd(d, (P-1)*(Q-1)) == 1:
        N = P*Q
        e = pow(d,-1,(P-1)*(Q-1))
        break
enc = pow(bytes_to_long(flag), e, N)
file = open('challenge.txt','w')
file.write(f'p = {p}\nenc = {enc}\nN = {N}')