from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from secret import flag, key

assert len(flag) == 32
assert len(key)  == 16

# should be equivalent to .hex() (probably)
to_hex = lambda x: "".join(hex(k)[2:] for k in x)

def encrypt(pt, key):
	aes = Cipher(AES(key), modes.ECB())
	enc = aes.encryptor()
	ct  = enc.update(pt)
	ct += enc.finalize()
	return ct

ct  = to_hex(encrypt(flag, key))
key = to_hex(key)

print(f'{ct  = }')
print(f'{key = }')

# ct  = '17c69a812e76d90e455a346c49e22fb6487d9245b3a90af42e67c7b7c3f2823'
# key = 'b5295cd71d2f7cedb377c2ab6cb93'
