from Crypto.Util.number import *

flag = bytes_to_long(open('flag.txt', 'rb').read())

factors = [getPrime(32) for i in range(32)]

n = 1

for factor in factors:
    n *= factor

e = 2**16+1

c = pow(flag, e, n)

out = open('output.txt', 'w')
out.write(f'{n = }\n')
out.write(f'{e = }\n')
out.write(f'{c = }\n')
out.close()