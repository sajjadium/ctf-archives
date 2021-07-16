import random
import math

def makeKey(n):
	privKey = [random.randint(1,4 ** n)];
	for i in range(1,n):
		privKey.append(random.randint(2 * privKey[-1],4 ** (n + i)));

	q = random.randint(privKey[-1] + 1,2 * privKey[-1]);
	r = random.randint(privKey[-1] + 1,2 * privKey[-1]);

	pubKey = [];
	for i in range(0,n):
		if(i < (n // 2)):
			pubKey.append(privKey[i] ^ q);
		else:
			pubKey.append(privKey[i] ^ r);

	return privKey,q,r,pubKey;

def enc(msg,pubKey):
	n = len(pubKey);
	cipher = 0;
	i = 0;
	a = 0;
	b = 0;
	for bit in msg:
		cipher ^= (int(bit) * pubKey[i]);
		if(i < (n // 2)):
			a ^= int(bit);
		else:
			b ^= int(bit);
		i += 1;

	return a,b,bin(cipher)[2:];

def dec(msg,privKey,q,r,a,b):
	msg ^= (q * a) ^ (r * b);
	pt = "";
	n = len(privKey)
	for i in range(n - 1,-1,-1):
		highestBit = 1 << (int)(math.log2(privKey[i]));
		pt = ('0','1')[(msg & highestBit) != 0] + pt;
		msg ^= ((msg & highestBit) != 0) * privKey[i];
	return bytes.fromhex(hex(int(pt,2))[2:]).decode("utf-8");

flag = open('flag.txt','rb').read();
binary = bin(int(flag.hex(),16))[2:];
keyPair = makeKey(len(binary));
print(keyPair[3]);
ct = enc(binary,keyPair[3]);
print(int(ct[2],2));