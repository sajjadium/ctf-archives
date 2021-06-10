from Crypto.Util.number import getPrime, bytes_to_long, inverse

p = getPrime(512)
q = getPrime(512)
n = p * q 

e = 65537

plain = open('plaintext.txt','r').read().lower()
ct = []
f = open('encrypted','w')
for i in plain:
	ct.append(pow(ord(i),e,n))
f.write('ct = ' + str(ct) + '\n')
#f.write('n = ' + str(n) + '\n')