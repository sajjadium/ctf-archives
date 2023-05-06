from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def keygen(nbit):
    p, q = [ getPrime(nbit) for _ in range(2)]
    n = p * q
    phi = (p-1)*(q-1)
    d = getPrime(1 << 8)
    e = inverse(d, phi)
    key = RSA.construct((n,e,d))
    return key


nbit = 512
key = keygen(nbit)
FLAG = open('flag.txt', 'rb').read()

cipher_rsa = PKCS1_v1_5.new(key)
enc = cipher_rsa.encrypt(FLAG)

open('flag.enc', 'w').write( enc.hex() )
open('pubkey.pem', 'wb').write( key.public_key().export_key('PEM') )
