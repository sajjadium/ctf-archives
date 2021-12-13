import string
import hashlib
import random

password2hash = b"REDACTED"
hashresult = hashlib.md5(password2hash).digest()
sha1 = hashlib.sha1(hashresult)
sha224 = hashlib.sha224(sha1.digest())
for i in range(0, 10):
	sha1 = hashlib.sha1(sha224.digest())
	sha224 = hashlib.sha224(sha1.digest())
output = sha224.hexdigest()
print("output: " + output)