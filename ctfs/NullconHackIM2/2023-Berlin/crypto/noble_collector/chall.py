from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long
import random

from secret import invitation

# Parameters
N = 2048

male = open('malenames-usa-top1000.txt','r').read().splitlines()
female = open('femalenames-usa-top1000.txt','r').read().splitlines()
family = open('familynames-usa-top1000.txt','r').read().splitlines()

def sample(l, k):
	random.shuffle(l)
	return ' '.join(l[:k])

def new_guest():
	name = ''
	gender = random.random()
	for _ in range(3):
		if random.random() < gender:
			name += random.choice(male) + ' '
		else:
			name += random.choice(female) + ' '
	name += random.choice(family)
	return name

key = RSA.generate(N, e = (1<<(1<<random.randint(0,4))) + 1)
name = new_guest()
msg = ('Dear %s' % name) + invitation
cipher = pow(bytes_to_long(msg.encode()), key.e, key.n)
print('Invitation for %s' % name)
print(key.publickey().export_key())
print(hex(cipher))
