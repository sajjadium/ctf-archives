FLAG = open('flag.txt', 'r').read()

flag_bytes = [ord(c) for c in FLAG]
flag_bits = ''.join([f'{num:08b}' for num in flag_bytes])

p = random_prime(2^256)
G = GF(p, modulus="primitive")
g = G.gen()
m = p-1

print(f'p: {p}')
for bit in flag_bits:
	x = G.random_element()
	if bit == '1':
		y = m-x
	else:
		y = G.random_element()

	print(f'{g^x}, {g^y}')

