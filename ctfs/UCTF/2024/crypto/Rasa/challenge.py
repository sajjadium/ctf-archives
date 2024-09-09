from Crypto.Util.number import bytes_to_long as b2l, getPrime

flag = b'uctf{test_flag}'

p = getPrime(1024)
q = getPrime(1024)

n = p*q

m1 = b2l(b'There were a mysterious underground cemetery found in Tabriz about 10 years ago near Blue Mosque while worker were digging in nearby locations')
m2 = b2l(b'It is an unknown cemetry which no historical records have registered it so far and it still remains a mystery for everyone. Can you help recover the secrets behind it?')
c1 = pow(m1, 3, n)
c2 = pow(m2, 3, n)

m = b2l(flag)
e1 = 0x10001
e2 = 0x8001

c3 = pow(m, e1, n)
c4 = pow(m, e2, n)

print(f"c1 = {c1}")
print(f"c2 = {c2}")
print(f"c3 = {c3}")
print(f"c4 = {c4}")
