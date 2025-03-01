from Crypto.Util.number import *

flag = open('flag.txt', 'rb').read()

p, q, s = getPrime(2048), getPrime(2048), getPrime(2048)
n1 = p * q
n2 = s * p
e = 2**16+1
d = pow(e, -1, (p-1)*(q-1))
c1 = pow(bytes_to_long(flag[:20]), e, n1)
c2 = pow(bytes_to_long(flag[20:]), e, n2)

out = open('output.txt', 'w')
out.write(f'{n1 = }\n')
out.write(f'{n2 = }\n')
out.write(f'{e = }\n')
out.write(f'{c1 = }\n')
out.write(f'{c2 = }\n')
out.close()