import random
import binascii

MAGIC = ?
K1 = b'\xae@\xb9\x1e\xb5\x98\x97\x81!d\x90\xed\xa9\x0bm~G\x92{y\xcd\x89\x9e\xec2\xb8\x1d\x13OB\x84\xbf\xfaI\xe1o~\x8f\xe40g!%Ri\xda\xd14J\x8aV\xc2x\x1dg\x07K\x1d\xcf\x86{Q\xaa\x00qW\xbb\xe0\xd7\xd8\x9b\x05\x88'
K2 = b"Q\xbfF\xe1Jgh~\xde\x9bo\x12V\xf4\x92\x81\xb8m\x84\x862va\x13\xcdG\xe2\xec\xb0\xbd{@\x05\xb6\x1e\x90\x81p\x1b\xcf\x98\xde\xda\xad\x96%.\xcb\xb5u\xa9=\x87\xe2\x98\xf8\xb4\xe20y\x84\xaeU\xff\x8e\xa8D\x1f('d\xfaw"
K3 = b"\xc6j\x0b_\x8e\xa1\xee7\x9d8M\xf9\xa2=])WI]'x)w\xc1\xc4-\xab\x06\xff\xbd\x1fi\xdb t\xe1\x9d\x14\x15\x8f\xb3\x03l\xe8\ru\xebm!\xc9\xcbX\n\xf8\x98m\x00\x996\x17\x1a\x04j\xb1&~\xa1\x8d.\xaa\xc7\xa6\x82"
K4 = b'9\x95\xf4\xa0q^\x11\xc8b\xc7\xb2\x06]\xc2\xa2\xd6\xa8\xb6\xa2\xd8\x87\xd6\x88>;\xd2T\xf9\x00B\xe0\x96$\xdf\x8b\x1eb\xeb\xeapL\xfc\x93\x17\xf2\x8a\x14\x92\xde64\xa7\xf5\x07g\x92\xfff\xc9\xe8\xe5\xfb\x95N\xd9\x81^r\xd1U8Y}'
K5 = b"9\xf8\xd2\x1a\x8d\xa14\xb9X\xccC\xe8\xf5X\x05l:\x8a\xf7\x00\xc4\xeb\x8f.\xb6\xa2\xfb\x9a\xbc?\x8f\x06\xe1\xdbY\xc2\xb2\xc1\x91p%y\xb7\xae/\xcf\x1e\x99r\xcc&$\xf3\x84\x155\x1fu.\xb3\x89\xdc\xbb\xb8\x1f\xfbN'\xe3\x90P\xf1k"
K6 = b'\xc6\x07-\xe5r^\xcbF\xa73\xbc\x17\n\xa7\xfa\x93\xc5u\x08\xff;\x14p\xd1I]\x04eC\xc0p\xf9\x1e$\xa6=M>n\x8f\xda\x86HQ\xd00\xe1f\x8d3\xd9\xdb\x0c{\xea\xca\xe0\x8a\xd1Lv#DG\xe0\x04\xb1\xd8\x1co\xaf\x0e\x94'


jokes = ["\nSheldon: Why are you crying?\nPenny: Because I'm stupid.\nSheldon: That's no reason to cry. One cries because one is sad. For example, I cry because others are stupid, and that makes me sad.", "Sheldon: Scissors cuts paper, paper covers rock, rock crushes lizard, lizard poisons Spock, Spock smashes scissors, scissors decapitates lizard, lizard eats paper, paper disproves Spock, Spock vaporizes rock, and as it always has, rock crushes scissors.","\nHoward: Sheldon, don't take this the wrong way, but, you're insane.\nLeonard: That may well be, but the fact is it wouldn't kill us to meet some new people.\nSheldon: For the record, it could kill us to meet new people. They could be murderers or the carriers of unusual pathogens. And I'm not insane, my mother had me tested."]


with open("flag.txt",'r') as f:
	flag = f.read().encode()

def foo(x, y, z, w):
	return bytes([(a&b&c&d | a&(b^255)&(c^255)&d | a&(b^255)&c&(d^255) | a&b&(c^255)&(d^255) | (a^255)&b&(c^255)&d | (a^255)&b&c&(d^255)) for a, b, c, d in zip(x, y, z, w)])
   
def gen_iv():
	iv_a = "{0:b}".format(random.getrandbits(MAGIC)).zfill(MAGIC) 
	print(f"Enjoy this random bits : {iv_a}")
	return iv_a, [b"\xff" * MAGIC if iv_a[i]=='1' else b"\x00" * MAGIC for i in range(MAGIC)]

def gen_keys():
	k = b"\x00"*MAGIC
	keys = []
	for i in range(MAGIC-1):
	    key = random.randbytes(MAGIC)
	    keys.append(key)
	    k = xor(k, xor(key,flag))
	keys.append(xor(k,flag))
	return keys
	
def xor(x, y):
    return bytes([a ^ b for a, b in zip(x, y)])
	

def my_input():
	inp = input()
	inp = binascii.unhexlify(inp)
	
	if len(inp) != MAGIC**2:
		print(random.choice(jokes))
		exit(0)
	
	return [inp[MAGIC*i:MAGIC*(i+1)] for i in range(MAGIC)]
	
def guardian(out, i, keys, intersection=b"\x00"*MAGIC):
	for j in range(i+1):
		intersection = xor(intersection, keys[j])
	return intersection == out
	

def main():

	print("Welcome to the Big Bang challenge!")

	iv_a, iv_b = gen_iv()
	keys = gen_keys()
	inp = my_input()
	
	output =  b"\x00"*MAGIC			
	for i in range(MAGIC):
		output = foo(output, foo(keys[i], foo(inp[i], iv_b[i], K5, K6), K3, K4), K1, K2)
		if not guardian(output, i, keys):
			print("Bazinga! You just fell to one of my classic pranks")
			exit(0)
	print(f"Congratulations, you are smarter than Sheldon!\nHere is your flag:\n{output}")

if __name__ == "__main__":
	try: 
		main()
	except Exception:
		print(random.choice(jokes))	
	finally:
		exit(0)
