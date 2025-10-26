from topsecret import n, secret_ids, flag
import math, random

assert all([math.gcd(num, n) == 1 for num in secret_ids])
assert len(secret_ids) == 32

vs = [pow(num, 2, n) for num in secret_ids]
print('n =', n)
print('vs =', vs)

correct = 0

for _ in range(1000):
	x = int(input('Pick a random r, give me x = r^2 (mod n): '))
	assert x > 0
	mask = '{:032b}'.format(random.getrandbits(32))
	print("Here's a random mask: ", mask)
	y = int(input('Now give me r*product of IDs with mask applied: '))
	assert y > 0
	# i.e: if bit i is 1, include id i in the product--otherwise, don't
	
	val = x
	for i in range(32):
		if mask[i] == '1':
			val = (val * vs[i]) % n
	if pow(y, 2, n) == val:
		correct += 1
		print('Phase', correct, 'of verification complete.')
	else:
		correct = 0
		print('Verification failed. Try again.')

	if correct >= 10:
		print('Verification succeeded. Welcome.')
		print(flag)
		break