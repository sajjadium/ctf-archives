from Crypto.Util.number import getPrime, bytes_to_long, getRandomNBitInteger
from flag import FLAG


p = getPrime(1024)
q = getPrime(1024)
n = p * q

e = 0x10001
c = pow(bytes_to_long(FLAG), e, n)

delta = getRandomNBitInteger(80)
x = p + delta

seq = []
val = 0
for i in range(5):
    seq.append(getRandomNBitInteger(1024))
    val = (val * x) % n
    val = (val + seq[-1]) % n

print('n=' + str(n))
print('e=' + str(e))
print('c=' + str(c))
print('seq=' + str(seq))
print('val=' + str(val))
