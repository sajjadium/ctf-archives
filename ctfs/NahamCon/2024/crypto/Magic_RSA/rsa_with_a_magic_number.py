from secrets import randbits
from sympy import nextprime

e = 3

def encrypt(inp):
	p = nextprime(randbits(2048))
	q = nextprime(randbits(2048))
	n = p * q
	enc = [pow(ord(c), e, n) for c in inp]
	return [n, enc]

plaintext = open('flag.txt').read()

with open('output.txt', 'w') as f:
    data = encrypt(plaintext)
    f.write(f'Semiprime:\nN: {data[0]}\nCiphertext:\n')
    f.write(''.join(f'{b} ' for b in data[1]))
    f.write('\n\n')