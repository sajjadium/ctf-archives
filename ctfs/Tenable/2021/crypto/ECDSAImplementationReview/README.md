

We found the following code and an output file. Can you extract the flag from the output file?

import ecdsa
import random
from Crypto.Cipher import AES
import binascii

def pad(m):
    return m+chr(16-len(m)%16)*(16-len(m)%16)

gen = ecdsa.NIST256p.generator
order = gen.order()
secret = random.randrange(1,order)
 
pub_key = ecdsa.ecdsa.Public_key(gen, gen * secret)
priv_key = ecdsa.ecdsa.Private_key(pub_key, secret)
 
nonce1 = random.randrange(1, 2**127)
nonce2 = nonce1
 
# randomly generate hash value
hash1 = random.randrange(1, order)
hash2 = random.randrange(1, order)
 
sig1 = priv_key.sign(hash1, nonce1)
sig2 = priv_key.sign(hash2, nonce2)

s1 = sig1.s
s2 = sig2.s

print("r: " + str(sig1.r))
print("s1: " + str(s1))
print("s2: " + str(s2))
print("")
print("hashes:")
print(hash1)
print(hash2)
print("")
print("order: " + str(order))
print("")

aes_key = secret.to_bytes(64, byteorder='little')[0:16]

ptxt =  pad("flag{example}")
IV = b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'
cipher = AES.new(aes_key, AES.MODE_CBC, IV)
ctxt = cipher.encrypt(ptxt.encode('utf-8'))

print("Encrypted Flag:")
print(binascii.hexlify(ctxt))

Output File Contents:

r: 50394691958404671760038142322836584427075094292966481588111912351250929073849
s1: 26685296872928422980209331126861228951100823826633336689685109679472227918891
s2: 40762052781056121604891649645502377037837029273276315084687606790921202237960

hashes:
777971358777664237997807487843929900983351335441289679035928005996851307115
91840683637030200077344423945857298017410109326488651848157059631440788354195

order: 115792089210356248762697446949407573529996955224135760342422259061068512044369

Encrypted Flag:
b'f3ccfd5877ec7eb886d5f9372e97224c43f4412ca8eaeb567f9b20dd5e0aabd5'


