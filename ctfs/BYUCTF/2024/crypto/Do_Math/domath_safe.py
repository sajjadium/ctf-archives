from Crypto.Util.number import *

p = getPrime(2048)
q = getPrime(2048)
e = 0x10001
n = p * q
d = pow(e, -1, (p-1)*(q-1))

msg = "byuctf{REDACTED}"
m = bytes_to_long(msg.encode('utf-8'))

c = pow(m, e, n)

print(c)
print()

hints = [p, q, e, n, d]
for _ in range(len(hints)):
    hints[_] = (hints[_] * getPrime(1024)) % n
    if hints[_] == 0: hints[_] = (hints[_] - 1) % n

print("Hints:")
print(hints)