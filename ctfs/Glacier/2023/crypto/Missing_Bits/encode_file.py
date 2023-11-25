from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import long_to_bytes

content = open("2048_key_original.priv", "rb").read()
key = RSA.import_key(content)

filecontent = open("plaintext_message", "rb").read()

ct = pow(bytes_to_long(filecontent), key.e, key.n)

open("ciphertext_message", "wb").write(long_to_bytes(ct))
