from flag import flag

from Crypto.Util.number import getPrime as gP

e1, e2 = 5*2, 5*3
assert len(flag) < 16
flag = "Wow good job the flag is (omg hype hype): vsctf{"+flag+"}"
p = gP(1024)
q = gP(1024)
n = p * q

m = int.from_bytes(flag.encode(), 'big')
c1 = pow(m, e1, n)
c2 = pow(m, e2, n)
print(f"n = {n}")
print(f"c1 = {c1}")
print(f"c2 = {c2}")
