from Crypto.Util.number import getPrime
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

from hashlib import md5
from math import prod
import sys

from secret import flag

key = getPrime(40)
haystack = [ getPrime(1024) for _ in range(300) ]
key_in_haystack = key * prod(haystack)

enc_flag = AES.new(
	key = md5(b"%d" % key).digest(),
	mode = AES.MODE_ECB
).encrypt(pad(flag, 16))

sys.set_int_max_str_digits(0)

print(f"enc_flag: {enc_flag.hex()}")
print(f"haystack: {key_in_haystack}")

exit(0)
