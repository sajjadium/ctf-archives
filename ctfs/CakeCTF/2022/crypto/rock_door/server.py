from Crypto.Util.number import getPrime, isPrime, getRandomRange, inverse, long_to_bytes
from hashlib import sha256
import os
import secrets


def h(s: bytes) -> int:
    return int(sha256(s).hexdigest(), 16)


q = 139595134938137125662213161156181357366667733392586047467709957620975239424132898952897224429799258317678109670496340581564934129688935033567814222358970953132902736791312678038626149091324686081666262178316573026988062772862825383991902447196467669508878604109723523126621328465807542441829202048500549865003
p = 2*q + 1

assert isPrime(p)
assert isPrime(q)

g = 2
flag = os.getenv("FLAG", "FakeCTF{hahaha_shshsh_hashman}")
x = h(secrets.token_bytes(16) + flag.encode())
y = pow(g, x, p)


def sign(m: bytes):
    z = h(m)
    k = h(long_to_bytes(x + z))
    r = h(long_to_bytes(pow(g, k, p)))
    s = (z + x*r) * inverse(k, q) % q
    return r, s


def verify(m: bytes, r: int, s: int):
    z = h(m)
    sinv = inverse(s, q)
    gk = pow(g, sinv*z, p) * pow(y, sinv*r, p) % p
    r2 = h(long_to_bytes(gk))
    return r == r2


print("p =", p)
print("g =", g)
print("y =", y)

print("=== sign ===")
m = input("m = ").strip().encode()
if b"goma" in m:
    quit()

r, s = sign(m)
# print("r =", r) do you really need?
print("s =", s)

print("=== verify ===")
m = input("m = ").strip().encode()
r = int(input("r = "))
s = int(input("s = "))
assert 0 < r < q
assert 0 < s < q

ok = verify(m, r, s)
if ok and m == b"hirake goma":
    print(flag)
elif ok:
    print("OK")
else:
    print("NG")
