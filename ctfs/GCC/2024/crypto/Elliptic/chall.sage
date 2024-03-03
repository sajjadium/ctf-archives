from Crypto.Util.number import isPrime, bytes_to_long
import json
from flag import flag

print("I'm pretty nice, I let you choose my curve parameters")

p = int(input("p = "))
a = int(input("a = "))
b = int(input("bl = "))

assert int(p).bit_length() > 128, "Send a bigger number"
assert isPrime(p), "Send a prime"


E = EllipticCurve(GF(p),[a,b])
G = E.gens()[0]
o = G.order()
l = factor(o)

assert int(l[-1][0]).bit_length() >= 0x56
flag_int = bytes_to_long(flag.lstrip(b"GCC{").rstrip(b"}"))

bin_flag = [int(val) for val in bin(flag_int)[2:]]

points = [E.random_element() for _ in range(len(bin_flag))]

s = G*0

for i,val in enumerate(bin_flag):
	if val == 1:
		s += points[i]

print(json.dumps({"values":[[int(a) for a in point.xy()] for point in points]}),flush=True)
print(s.xy(),flush=True)