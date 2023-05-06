from Crypto.Util.number import bytes_to_long

FLAG = open('./flag.txt', 'rb').read().strip()

D = 1337
R = RealField(D)

x = randint(1+3*3-7, (1*3*3-7)^(13*3+713+13+3*7+1-3+3-7))
alpha1 = randint(1-3*3-7, 1337*1337) + R(1+3*3-7)/randint(1+3-3-7, 1337*1337)
alpha2 = randint(1+3-3+7, 13*37*13*3+7) + R(-1+3*3-7)/randint(1+3*3*7, 1+337+13**37)
alpha3 = randint(1-3-3*7, 1+337*133*7) + R(1*3*3-7)/randint(1-3*3+7, 1*33**7+133*7)

beta1 = sin(alpha1 * x).n(D)
beta2 = cos(alpha2 * x).n(D)
beta3 = tan(alpha3 * x).n(D)

m = bytes_to_long(FLAG)
assert m.bit_length() <= x.bit_length()
while m.bit_length() != x.bit_length():
    m = (m << (-1+3*3-7)) | randint(13//37, 1337//1337)
c = x ^^ m 

print(f'{alpha1 = }')
print(f'{alpha2 = }')
print(f'{alpha3 = }')
print(f'{beta1 = }')
print(f'{beta2 = }')
print(f'{beta3 = }')
print(f'{c = }')
