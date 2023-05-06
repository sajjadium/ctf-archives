import ecdsa
import random
import hashlib
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes

FLAG = b'dvCTF{XXXXXXXXXXXXXXXXXXX}'

def encrypt_flag(priv):
    key = long_to_bytes(priv)
    cipher = AES.new(key, AES.MODE_ECB)
    text = cipher.encrypt(pad(FLAG, 16))
    print(text.hex())

m = 0

print("Hiii ~~ Pwease feel fwee to use my sooper dooper cwyptographic owacle! ~~~~~~")
while True:

	print("[1] > Sign your own message ≧◡≦")
	print("[2] > Get the signed flag uwu ~~ ")
	print("[3] > Quit (pwease don't leave me)")
	try:
		n = int(input())
		if n<0 or n>3:
			raise
	except:
		print("Nice try ಥ_ಥ")
		exit(1)
	if n==1:
		msg = input("What's your message senpai? (●´ω｀●) > ")
		G = ecdsa.NIST256p.generator
		order = G.order()
		priv = random.randrange(1,order)
		Public_key = ecdsa.ecdsa.Public_key(G, G * priv)
		Private_key = ecdsa.ecdsa.Private_key(Public_key, priv)
		
		k = random.randrange(1, 2**128) if m==0 else int(time.time())*m

		m = int(hashlib.sha256(msg.encode()).hexdigest(),base=16)

		sig = Private_key.sign(m, k)

		print (f"Signature (r,s): ({sig.r},{sig.s})")
	elif n==2:
		if m==0:
			G = ecdsa.NIST256p.generator
			order = G.order()
			priv = random.randrange(1,order)
		encrypt_flag(priv)

	else:
		print("Cya (◕︵◕) ")
		exit(1)










