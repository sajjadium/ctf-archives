from Crypto.PublicKey import RSA
from secret import flag
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import inverse
from binascii import hexlify

key1 = RSA.import_key(open('key1.pem','rb').read())
key2 = RSA.import_key(open('key2.pem','rb').read())

msg1 = flag[:len(flag)//2]
msg2 = flag[len(flag)//2:]

cryptor = PKCS1_OAEP.new(key1)
c1 = cryptor.encrypt(msg1)

cryptor = PKCS1_OAEP.new(key2)
c2 = cryptor.encrypt(msg2)

writer = open('ciphers','wb')
writer.write(hexlify(c1) + b'\n' + hexlify(c2))
writer.close()
