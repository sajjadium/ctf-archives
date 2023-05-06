import random
import flag
import collections
import os
import pow

def xorshift64(x):
	x ^= (x << 13) & 0xffffffffffffffff
	x ^= (x >> 7) & 0xffffffffffffffff
	x ^= (x << 17) & 0xffffffffffffffff
	return x

def main():
	r = os.urandom(10)
	random.seed(r)
	
	SEEDS = 18
	seed = input("give me the seed: ")
	seed = seed.strip()

	if(len(seed)) != SEEDS:
		print("seed should be "+str(SEEDS)+" bytes long!")
		exit()

	seed = list(seed)
	random.shuffle(seed)
	
	counts = collections.Counter(seed)
	if counts.most_common()[0][1] > 3:
			print ("You can't use the same number more than 3 times!")
			exit()
	
	int16 = lambda x: int(x,16)
	seed = list(map(int16,seed))
	S = 0x0
	for i in range(SEEDS):
		S*=16
		S+=seed[i]
				
	count = 2+seed[0]+seed[1]
	for i in range(count):
		S=xorshift64(S)	
	
	last = S & 0xFFFF
	print("The last 2 bytes are: "+str(last))
	
	check = int(input("give me the number: "))
	if check == S:
		print(flag.flag)
	else:
		print("Nope!")

if __name__ == '__main__':
	pow.check_pow(27)
	main()
