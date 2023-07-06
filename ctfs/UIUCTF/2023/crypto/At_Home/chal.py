from Crypto.Util.number import getRandomNBitInteger

flag = int.from_bytes(b"uiuctf{******************}", "big")

a = getRandomNBitInteger(256)
b = getRandomNBitInteger(256)
a_ = getRandomNBitInteger(256)
b_ = getRandomNBitInteger(256)

M = a * b - 1
e = a_ * M + a
d = b_ * M + b

n = (e * d - 1) // M

c = (flag * e) % n

print(f"{e = }")
print(f"{n = }")
print(f"{c = }")
