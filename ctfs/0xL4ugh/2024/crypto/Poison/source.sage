from random import *  
from Crypto.Util.number import * 
flag = b'REDACTED'
#DEFINITION
K = GF(0xfffffffffffffffffffffffffffffffeffffffffffffffff);a = K(0xfffffffffffffffffffffffffffffffefffffffffffffffc);b = K(0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1)
E = EllipticCurve(K, (a, b))
G = E(0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012, 0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811)

#DAMAGE 
def poison(val,index): 
	val = list(val)
	if val[index] == '1': 
		val[index] = '0'
	else: 
		val[index] = '1'
	return ''.join(val)

my_priv = bin(bytes_to_long(flag))[2:]
ms = []
C1s = []
C2s = []
decs = []

count = 0 

while count < len(my_priv):
	try: 
		k = randint(2, G.order()-2)
		Q = int(my_priv,2)*G
		M = randint(2,G.order()-2)
		M = E.lift_x(Integer(M));ms.append((M[0],M[1]))
		
		C1 = k*G;C1s.append((C1[0],C1[1]))
		C2 = M + k*Q;C2s.append((C2[0],C2[1]))

		ind = len(my_priv)-1-count
		new_priv = poison(my_priv,ind)
		new_priv = int(new_priv,2)
		dec = (C2 - (new_priv)*C1);decs.append((dec[0],dec[1]))
		count +=1 
	except: 
		pass

with open('out.txt','w') as f: 
	f.write(f'ms={ms}\n')
	f.write(f'C1s={C1s}\n')
	f.write(f'C2s={C2s}\n')
	f.write(f'decs={decs}')