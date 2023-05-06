from Crypto.PublicKey import ECC
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint
from blake3 import blake3
import base64 as b64
import traffic
import ecdsa

secure_message = traffic.get_msg()

sign_pub= None
with open('key.pub','rb') as f:
	sign_pub=f.read()
ver=ecdsa.VerifyingKey.from_pem(sign_pub)


def int_to_bytes(x: int) -> bytes:
	return x.to_bytes()
    
def bytes_to_int(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


def H1(msg):
	hasher = blake3()
	hasher.update(b'Salty')
	hasher.update(msg)
	return hasher.digest()


def H2(c, msg):
	hasher = blake3()
	hasher.update(int.to_bytes(c,32,'big'))
	hasher.update(msg)
	return hasher.digest()

def tokenize(msg):
	return [msg[i:i+8] for i in range(len(msg)-8)]

class ECC_G():
	def __init__(self):
		pass

	def generate(self):
		self.g = ECC.generate(curve='p256').pointQ
		self.h = ECC.generate(curve='p256').pointQ


	def get_public(self):
		return (self.g,self.h)



class SR_Oracle():
	def __init__(self,g,h):
		self.g = g
		self.h = h
		self.k_sr = bytes_to_int(get_random_bytes(32))

	def compute_intermediate_rule(self,Ri):
		return Ri*self.k_sr

	def compute_obfuscated_tokens(self,ti_list):
		Ti_list=[]
		c = randint(0,2**32)
		for i in range(len(ti_list)):
			encrypted = int_to_bytes(self._encrypt(ti_list[i]).x)
			Ti_list.append(H2(c+i,encrypted))
		return (c,Ti_list)

	def _encrypt(self,msg):
		return (g*bytes_to_int(H1(msg))+h)*self.k_sr



if __name__ == '__main__':
	n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

	RG = ECC_G()
	RG.generate()
	g,h = RG.get_public()
	SR = SR_Oracle(g,h)

	print("Hello MiddleBox. Here is my g and h:")
	print(hex(g.x)[2:],hex(g.y)[2:])
	print(hex(h.x)[2:],hex(h.y)[2:])


	n = 157
	n_traf = True
	try:
		while True:
			print("Menu:")
			print("1. Obfuscate rule (Will accept exactly "+str(n)+" more)")
			print("2. Get traffic")
			i = input().strip()
			if i == '1':
				n-=1
				if n < 1:
					exit()
				R = input().strip()
				Rinit = R.encode('utf-8') # 2lazy2compress
				R = R.split(' ')
				R = ECC.EccPoint(int(R[0],16),int(R[1],16))
				sig = b64.b64decode(input().strip())

				if R == g or R == h:
					print("Rule entropy too small.")
					exit()

				if not ver.verify(sig,Rinit):
					exit()

				s1 = SR.compute_intermediate_rule(R)
				print(hex(s1.x)[2:],hex(s1.y)[2:])
			elif i == '2':
				if n_traf:
					n_traf = False 
					c,Ti=SR.compute_obfuscated_tokens(tokenize(secure_message))
					print(str(c)+'|',end='')
					print(b64.b64encode(b''.join(Ti)).decode('utf-8'))
			else:
				exit()
	except:
		exit()
