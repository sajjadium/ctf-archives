from Crypto.Util import number

def fastpow(b, p, mod):
    # idk this is like repeated squaring or something i heard it makes pow faster
    a = 1
    while p:
        p >>= 1
        b = (b*b)%mod
        if p&1:
            a = (a*b)%mod
    return a

p = number.getPrime(100)
q = number.getPrime(100)
n = p*q
e = 65537
m = int.from_bytes(open("flag.txt", "r").readline().strip().encode(), 'big')
assert(m < n)
c = fastpow(m, e, n)

print("n =", n)
print("e =", e)
print("c =", c)
