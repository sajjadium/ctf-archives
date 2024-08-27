mod = int(input('Public mod: '))
base = int(input('Public base: '))

a_secret = int(input('A secret: '))
b_secret = int(input('B secret: '))

a_public = (base ** a_secret) % mod
b_public = (base ** b_secret) % mod

print('=================')

print('A public = ' + str(a_public))
print('B public = ' + str(b_public))

a_shared = (b_public ** a_secret) % mod
b_shared = (a_public ** b_secret) % mod

print('A shared secret = ' + str(a_shared))
print('B shared secret = ' + str(b_shared))
