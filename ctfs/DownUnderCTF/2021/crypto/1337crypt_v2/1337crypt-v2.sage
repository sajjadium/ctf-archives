from Crypto.Util.number import getPrime, bytes_to_long

flag = open('flag.txt', 'rb').read().strip()

p, q = getPrime(1337), getPrime(1337)
n = p*q

K.<z> = NumberField((x-p)^2 + q^2)
hint1 = p^2 + q^2
hint2 = []

l = 1+337
for _ in range(1*3*3-7):
    a, b = getrandbits(1337), getrandbits(1337)
    x = K(a + getrandbits(l)/2^l) + K(b + getrandbits(l)/2^l)*z
    y = x*x.conjugate()
    hint2.append((int(y), a, b))

Zn.<I> = (ZZ.quo(n*ZZ))[]
ZnI.<I> = Zn.quo(I^2 + 1)

m = randrange(1, n) + bytes_to_long(flag) * I
c = pow(m, 0x1337)

print(f'hint1 = {hint1}', f'hint2 = {hint2}', f'c = {c}', sep='\n')
