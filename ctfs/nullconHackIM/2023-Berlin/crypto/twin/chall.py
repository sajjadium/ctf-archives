from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long
from binascii import hexlify

from secret import flag

key1 = RSA.import_key(open('key1.pem','rb').read())
key2 = RSA.import_key(open('key2.pem','rb').read())

c1 = pow(bytes_to_long(flag), key1.e, key1.n)
c2 = pow(bytes_to_long(flag), key2.e, key2.n)

writer = open('ciphers','w')
writer.write('%d\n%d' % (c1, c2))
writer.close()
