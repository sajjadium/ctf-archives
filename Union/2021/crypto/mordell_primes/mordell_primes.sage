from Crypto.Util.number import bytes_to_long
from secrets import k, FLAG

assert k < 2^128
assert FLAG.startswith(b'union{')

E = EllipticCurve(QQ,[0,1,0,78,-16])
P = E(1,8)
Q = k*P
R = (k+1)*P

p = Q[0].numerator()
q = R[0].numerator()

assert is_prime(p)
assert is_prime(q)

e = 0x10001
N = p*q
m = bytes_to_long(FLAG)
c = pow(m,e,N)

print(f'N = {N}')
print(f'c = {c}')
