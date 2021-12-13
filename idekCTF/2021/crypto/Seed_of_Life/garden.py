import random

seed = REDACTED
assert seed in range(10000000)
random.seed(seed)
for i in range(19):
	random.seed(random.random())
seedtosave = random.random()
print("share1:")
for add in range(0, 1000):
	random.seed(seedtosave+add)
	for i in range(0, 100):
		print(random.random())
print("share2:")
for add in range(0, 1000):
	random.seed(seedtosave-add)
	for i in range(0, 1000):
		print(random.random())
print("share3:")
random.seed(seedtosave)
for i in range(0, 100):
	print(random.random()*100)