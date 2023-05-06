from Crypto.Util.number import getPrime, bytes_to_long
from private import flag

def prod(lst):
	ret = 1
	for num in lst:
		ret *= num
	return ret

m = bytes_to_long(flag)
primes = [getPrime(32) for _ in range(128)]
n = prod(primes)
e = 65537
print(n)
print(pow(m, e, n))