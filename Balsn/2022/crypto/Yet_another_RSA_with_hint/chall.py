from Crypto.Util.number import *
from secret import flag

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 0x10001
c = pow(bytes_to_long(flag), e, n)

def digitsSum(n, base):
	ret = 0
	while n:
		ret += n % base
		n //= base
	return ret

hint = [digitsSum(p, i) for i in range(2, 200)]

print(f"{n = }")
print(f"{e = }")
print(f"{c = }")
print(f"{hint = }")