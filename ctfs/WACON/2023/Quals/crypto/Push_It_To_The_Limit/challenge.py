from Crypto.Util.number import bytes_to_long, getStrongPrime

with open("flag.txt", "rb") as f:
    m = bytes_to_long(f.read())

SIZE = 1024
p = getStrongPrime(SIZE)
q = getStrongPrime(SIZE)
n = p * q
e = 0x10001
c = pow(m, e, n)

p_msb = p - p % (2 ** (SIZE // 2))

print(f"{n = }")
print(f"{c = }")
print(f"{p_msb = }")
