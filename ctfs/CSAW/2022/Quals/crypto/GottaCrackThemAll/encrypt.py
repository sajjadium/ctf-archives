with open('key.txt','rb') as f:
	key = f.read()

def encrypt(plain):
	return b''.join((ord(x) ^ y).to_bytes(1,'big') for (x,y) in zip(plain,key))
